import time
from django.test import TestCase
from apps.simulation.whatif_service import simulate_what_if
from apps.data_layer.models import Field
from apps.accounts.models import User, FarmerProfile
from apps.zones.models import Zone

class SimulationAppTests(TestCase):
    def setUp(self):
        self.zone = Zone.objects.create(name='Simulation Zone', code='SIM', region_group='WESTERN')
        self.user = User.objects.create_user(username='sim_farmer', role=User.Role.FARMER)
        self.farmer = FarmerProfile.objects.create(user=self.user, zone=self.zone)
        self.field = Field.objects.create(
            name='Sim Field', latitude=11.01, longitude=76.96, crop_type='rice', owner=self.farmer
        )

    def test_whatif_execution_under_1_point_5_seconds(self):
        start = time.time()
        res = simulate_what_if(self.field.id, {
            'irrigation_delta_pct': 25,
            'harvest_delay_days': 5,
            'fertilizer_delta_pct': 10
        })
        duration = time.time() - start
        self.assertLess(duration, 1.5)
        self.assertNotIn('error', res)
        self.assertIn('baseline', res)
        self.assertIn('simulated', res)
        self.assertIn('delta_pct', res)
        self.assertIn('new_growth_stage', res)

    def test_irrigation_plateau_behavior(self):
        # Normal moderate irrigation (+20%) gives positive response
        res_mod = simulate_what_if(self.field.id, {
            'irrigation_delta_pct': 20,
            'harvest_delay_days': 0,
            'fertilizer_delta_pct': 0
        })
        # Extreme excessive irrigation (+120%) causes waterlogging penalty
        res_extreme = simulate_what_if(self.field.id, {
            'irrigation_delta_pct': 120,
            'harvest_delay_days': 0,
            'fertilizer_delta_pct': 0
        })
        # The extreme irrigation yields lower than or plateaus compared to optimal moderate
        self.assertLess(res_extreme['simulated']['yield_mean'], res_mod['simulated']['yield_mean'] * 1.05)

    def test_harvest_delay_pest_warning(self):
        res_delay = simulate_what_if(self.field.id, {
            'irrigation_delta_pct': 0,
            'harvest_delay_days': 25, # >20 days
            'fertilizer_delta_pct': 0
        })
        self.assertIsNotNone(res_delay['warning'])
        self.assertIn('pest', res_delay['warning'].lower())
        self.assertLess(res_delay['delta_pct'], 0)

    def test_boundary_inputs(self):
        res_bound = simulate_what_if(self.field.id, {
            'irrigation_delta_pct': -150, # out of normal bounds
            'harvest_delay_days': 100,
            'fertilizer_delta_pct': -200
        })
        self.assertNotIn('error', res_bound)
        self.assertGreater(res_bound['simulated']['yield_mean'], 0)
        self.assertLessEqual(res_bound['new_growth_stage'], 100.0)
