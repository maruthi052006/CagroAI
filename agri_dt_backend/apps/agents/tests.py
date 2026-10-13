from django.test import TestCase
from apps.agents.agents import (
    CropGrowthAgent, WeatherAgent, PestDiseaseAgent, YieldForecastAgent
)

class CognitiveAgentsTests(TestCase):
    def setUp(self):
        self.crop_agent = CropGrowthAgent()
        self.weather_agent = WeatherAgent()
        self.pest_agent = PestDiseaseAgent()
        self.yield_agent = YieldForecastAgent()

    def test_agents_across_five_crop_types(self):
        crops = ["rice", "wheat", "maize", "cotton", "groundnut"]
        for crop in crops:
            field_data = {
                'crop_type': crop,
                'temperature': 26.0,
                'soil_moisture': 60.0,
                'rainfall': 15.0,
                'humidity': 65.0,
                'source': 'REAL'
            }

            # 1. Crop Growth Agent
            cg = self.crop_agent.run(field_data)
            self.assertGreater(cg['growth_stage'], 0)
            self.assertLessEqual(cg['growth_stage'], 100)
            self.assertGreater(cg['biomass_estimate'], 0)
            self.assertIn('sources', cg)
            self.assertEqual(cg['sources']['growth_stage'], 'PREDICTED')

            # 2. Weather Agent
            w = self.weather_agent.run(field_data)
            self.assertEqual(w['rain_forecast_7day'], 105.0)
            self.assertIn(w['temp_risk_level'], ['low', 'medium', 'high'])
            self.assertIn('sources', w)
            self.assertEqual(w['sources']['rain_forecast_7day'], 'PREDICTED')

            # 3. Pest Disease Agent
            p = self.pest_agent.run(field_data)
            self.assertGreaterEqual(p['pest_risk_score'], 0.0)
            self.assertLessEqual(p['pest_risk_score'], 1.0)
            self.assertIn(p['risk_category'], ['low', 'medium', 'high'])
            self.assertEqual(p['sources']['risk_category'], 'RULE_BASED_TNAU')

            # 4. Yield Forecast Agent
            y = self.yield_agent.run(field_data)
            self.assertGreater(y['yield_mean'], 1000)
            self.assertLessEqual(y['yield_p10'], y['yield_mean'])
            self.assertGreaterEqual(y['yield_p90'], y['yield_mean'])
            self.assertEqual(len(y['distribution_samples']), 15)
            self.assertEqual(y['sources']['yield_mean'], 'PREDICTED')
            self.assertEqual(y['sources']['yield_p10'], 'SIMULATED')

    def test_extreme_weather_behavior(self):
        extreme_heat = {
            'crop_type': 'wheat',
            'temperature': 44.0,
            'soil_moisture': 20.0,
            'rainfall': 0.0,
            'humidity': 25.0
        }
        w_res = self.weather_agent.run(extreme_heat)
        self.assertEqual(w_res['temp_risk_level'], 'high')
        self.assertTrue(w_res['extreme_event_risk'])

        cg_res = self.crop_agent.run(extreme_heat)
        self.assertLess(cg_res['confidence'], 0.6)

    def test_high_humidity_pest_trigger(self):
        fungal_conditions = {
            'crop_type': 'rice',
            'temperature': 25.0,
            'humidity': 88.0, # >75%
            'soil_moisture': 80.0
        }
        p_res = self.pest_agent.run(fungal_conditions)
        self.assertEqual(p_res['risk_category'], 'high')
        self.assertGreaterEqual(p_res['pest_risk_score'], 0.7)
        self.assertIn('blast', p_res['primary_pathogen'].lower())
