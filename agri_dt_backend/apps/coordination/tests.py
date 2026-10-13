from django.test import TestCase
from apps.coordination.conflict_detector import detect_conflicts
from apps.coordination.resolver import resolve_outputs
from apps.coordination.trust_score import compute_trust_score
from apps.coordination.farm_health import compute_farm_health_index
from apps.data_layer.models import Field
from apps.accounts.models import User, FarmerProfile
from apps.zones.models import Zone

class CoordinationLayerTests(TestCase):
    def setUp(self):
        self.zone = Zone.objects.create(name='Delta Zone', code='DEL', region_group='DELTA')
        self.user = User.objects.create_user(username='coord_farmer', role=User.Role.FARMER)
        self.farmer = FarmerProfile.objects.create(user=self.user, zone=self.zone)
        self.field = Field.objects.create(
            name='Test Field', latitude=10.78, longitude=79.13, crop_type='rice', owner=self.farmer
        )

    def test_conflict_scenario_irrigation_vs_rain(self):
        agent_outputs = {
            'crop_growth': {'growth_stage': 45.0, 'reason': 'Vegetative need', 'confidence': 0.85},
            'weather': {'rain_forecast_7day': 35.0, 'temp_risk_level': 'low', 'reason': 'Rain coming'},
            'pest': {'pest_risk_score': 0.15, 'risk_category': 'low', 'reason': 'Low pest'},
            'yield': {'yield_mean': 4800.0, 'yield_p10': 4300.0, 'yield_p90': 5300.0, 'confidence': 0.88}
        }
        conflicts = detect_conflicts(agent_outputs)
        self.assertGreaterEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]['issue'], 'irrigation_vs_rain')
        self.assertIn('rainfall', conflicts[0]['resolution'].lower())

    def test_conflict_scenario_pest_vs_humidity(self):
        agent_outputs = {
            'crop_growth': {'growth_stage': 60.0, 'reason': 'Growing', 'confidence': 0.85},
            'weather': {'rain_forecast_7day': 25.0, 'temp_risk_level': 'low', 'reason': 'Precipitation'},
            'pest': {'pest_risk_score': 0.85, 'risk_category': 'high', 'primary_pathogen': 'Fungal blast', 'reason': 'Severe fungal risk'},
            'yield': {'yield_mean': 4200.0, 'yield_p10': 3800.0, 'yield_p90': 4600.0, 'confidence': 0.85}
        }
        conflicts = detect_conflicts(agent_outputs)
        issues = [c['issue'] for c in conflicts]
        self.assertIn('pest_vs_humidity', issues)

    def test_resolver_generates_structured_reasoning_trace(self):
        agent_outputs = {
            'crop_growth': {'growth_stage': 50.0, 'reason': 'Thermal match 0.88.', 'confidence': 0.88},
            'weather': {'rain_forecast_7day': 25.0, 'temp_risk_level': 'low', 'reason': '25mm projected.'},
            'pest': {'pest_risk_score': 0.20, 'risk_category': 'low', 'reason': 'Negligible pest.'},
            'yield': {'yield_mean': 4600.0, 'yield_p10': 4100.0, 'yield_p90': 5100.0, 'confidence': 0.89}
        }
        resolved = resolve_outputs(agent_outputs)
        self.assertIn('reasoning_trace', resolved)
        trace = resolved['reasoning_trace']
        self.assertGreaterEqual(len(trace), 5)
        # Verify trace structure required by EXAI in Phase 5
        for step in trace:
            self.assertIn('step', step)
            self.assertIn('actor', step)
            self.assertIn('statement', step)
            self.assertIn('conflict', step)
            self.assertIn('final', step)
        self.assertTrue(trace[-1]['final'])
        self.assertEqual(trace[-1]['actor'], 'CognitiveResolver')

    def test_trust_score_edge_cases(self):
        # Case 1: High conflicts, poor quality
        bad_outputs = {
            'crop_growth': {'growth_stage': 40.0, 'confidence': 0.4},
            'weather': {'rain_forecast_7day': 40.0, 'temp_risk_level': 'high'},
            'pest': {'pest_risk_score': 0.90, 'risk_category': 'high'},
            'yield': {'yield_mean': 3000.0, 'yield_p10': 2500.0, 'yield_p90': 3500.0}
        }
        coord_res = resolve_outputs(bad_outputs)
        bad_field_data = {'crop_type': 'rice', 'temperature': 65.0} # severe outlier
        trust_bad = compute_trust_score(bad_outputs, self.field, coord_res, bad_field_data)
        self.assertIn(trust_bad['trust_label'], ['LOW', 'MODERATE'])
        self.assertLess(trust_bad['trust_score'], 70)

        # Case 2: Clean harmonic data
        good_outputs = {
            'crop_growth': {'growth_stage': 65.0, 'confidence': 0.95},
            'weather': {'rain_forecast_7day': 5.0, 'temp_risk_level': 'low'},
            'pest': {'pest_risk_score': 0.05, 'risk_category': 'low'},
            'yield': {'yield_mean': 4800.0, 'yield_p10': 4400.0, 'yield_p90': 5200.0}
        }
        coord_good = resolve_outputs(good_outputs)
        good_field_data = {'crop_type': 'rice', 'temperature': 26.0, 'rainfall': 5.0, 'humidity': 60.0, 'soil_moisture': 65.0}
        trust_good = compute_trust_score(good_outputs, self.field, coord_good, good_field_data)
        self.assertEqual(trust_good['trust_label'], 'HIGH')
        self.assertGreaterEqual(trust_good['trust_score'], 75)

    def test_farm_health_weighting(self):
        outputs = {
            'crop_growth': {'confidence': 0.9, 'growth_stage': 70.0},
            'weather': {'temp_risk_level': 'low', 'extreme_event_risk': False},
            'pest': {'pest_risk_score': 0.10}
        }
        field_data = {'soil_moisture': 60.0}
        health = compute_farm_health_index(outputs, field_data)
        self.assertIn('score', health)
        self.assertIn('rating', health)
        self.assertGreaterEqual(health['score'], 80)
        self.assertEqual(health['rating'], 'OPTIMAL')
        self.assertIn('breakdown', health)
        self.assertIn('crop_health', health['breakdown'])
        self.assertIn('water_soil_health', health['breakdown'])
        self.assertIn('pest_disease_health', health['breakdown'])
        self.assertIn('climate_stability', health['breakdown'])

    def test_farm_health_stressed_and_critical(self):
        # Stressed conditions
        outputs_stressed = {
            'crop_growth': {'confidence': 0.4, 'growth_stage': 20.0},
            'weather': {'temp_risk_level': 'high', 'extreme_event_risk': True},
            'pest': {'pest_risk_score': 0.75}
        }
        field_stressed = {'soil_moisture': 20.0} # dry
        h_stressed = compute_farm_health_index(outputs_stressed, field_stressed)
        self.assertIn(h_stressed['rating'], ['STRESSED', 'CRITICAL'])

    def test_heat_stress_vs_harvest_conflict(self):
        heat_outputs = {
            'crop_growth': {'growth_stage': 90.0, 'reason': 'Mature stage'},
            'weather': {'rain_forecast_7day': 0.0, 'temp_risk_level': 'high', 'extreme_event_risk': True},
            'pest': {'pest_risk_score': 0.1},
            'yield': {'yield_mean': 4500.0}
        }
        conflicts = detect_conflicts(heat_outputs)
        issues = [c['issue'] for c in conflicts]
        self.assertIn('heat_stress_vs_harvest', issues)
        resolved = resolve_outputs(heat_outputs)
        self.assertIn('extreme_weather_risk', resolved['risk_flags'])

