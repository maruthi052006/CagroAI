from django.test import TestCase
from rest_framework.test import APIClient
from apps.data_layer.models import Field
from apps.accounts.models import User, FarmerProfile
from apps.zones.models import Zone
from apps.api.models import MLModelVersion

class ApiEndpointsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.zone = Zone.objects.create(name='API Zone', code='API', region_group='NORTHERN')
        self.user = User.objects.create_user(username='api_farmer', role=User.Role.FARMER)
        self.farmer = FarmerProfile.objects.create(user=self.user, zone=self.zone)
        self.field = Field.objects.create(
            name='API Field', latitude=13.08, longitude=80.27, crop_type='rice', owner=self.farmer
        )

    def test_predict_endpoint(self):
        response = self.client.post('/api/predict/', {'field_id': self.field.id}, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('final_recommendation', data)
        self.assertIn('yield_prediction', data)
        self.assertIn('reasoning_trace', data)
        self.assertIn('trust_score', data)
        self.assertIn('farm_health_index', data)
        self.assertIn('provenance_summary', data)
        self.assertIn('agent_outputs', data)

    def test_crop_registry_returns_forty_crops(self):
        response = self.client.get('/api/crop-registry/')
        self.assertEqual(response.status_code, 200)
        crops = response.json()
        self.assertEqual(len(crops), 40)
        archetypes = set(c['archetype'] for c in crops)
        self.assertEqual(len(archetypes), 9)

    def test_what_if_endpoint(self):
        payload = {
            'field_id': self.field.id,
            'adjustments': {
                'irrigation_delta_pct': 10,
                'harvest_delay_days': 0,
                'fertilizer_delta_pct': 5
            }
        }
        response = self.client.post('/api/simulate/what-if/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('baseline', data)
        self.assertIn('simulated', data)

    def test_timeline_endpoint(self):
        response = self.client.get(f'/api/simulation/{self.field.id}/timeline/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('timeline', data)
        self.assertEqual(len(data['timeline']), 12)

    def test_dataset_info_endpoint(self):
        response = self.client.get('/api/dataset-info/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_files'], 22)
        self.assertEqual(data['grounded_crops'], 26)

    def test_model_registry_endpoint(self):
        response = self.client.get('/api/model-registry/')
        self.assertEqual(response.status_code, 200)
        models = response.json()
        self.assertGreaterEqual(len(models), 1)
        self.assertIn('metrics', models[0])

    def test_decision_and_outcome_lifecycle(self):
        # 1. Run prediction to generate PredictionLog
        pred_res = self.client.post('/api/predict/', {'field_id': self.field.id}, format='json')
        self.assertEqual(pred_res.status_code, 200)
        from apps.data_layer.models import PredictionLog
        pred_log = PredictionLog.objects.filter(field=self.field).first()
        self.assertIsNotNone(pred_log)

        # 2. Respond to decision
        dec_res = self.client.post(f'/api/decisions/{pred_log.id}/respond/', {
            'farmer_decision': 'APPROVED',
            'decision_reason': 'Followed recommended irrigation cycle'
        }, format='json')
        self.assertEqual(dec_res.status_code, 200)
        self.assertEqual(dec_res.json()['farmer_decision'], 'APPROVED')

        # 3. Check decisions list
        list_res = self.client.get(f'/api/decisions/?field_id={self.field.id}')
        self.assertEqual(list_res.status_code, 200)
        self.assertEqual(len(list_res.json()), 1)

        # 4. Record 3 harvest outcomes to trigger field-level calibration
        self.client.post(f'/api/outcomes/{self.field.id}/record/', {
            'actual_yield': 4200.0,
            'season_year': 2024,
            'notes': 'Season 1'
        }, format='json')
        self.client.post(f'/api/outcomes/{self.field.id}/record/', {
            'actual_yield': 4100.0,
            'season_year': 2025,
            'notes': 'Season 2'
        }, format='json')
        self.client.post(f'/api/outcomes/{self.field.id}/record/', {
            'actual_yield': 4300.0,
            'season_year': 2026,
            'notes': 'Season 3'
        }, format='json')

        # 5. Check accuracy summary
        acc_res = self.client.get(f'/api/outcomes/accuracy-summary/?field_id={self.field.id}')
        self.assertEqual(acc_res.status_code, 200)
        acc_data = acc_res.json()
        self.assertEqual(acc_data['total_outcomes'], 3)
        self.assertTrue(acc_data['calibrated'])
        self.assertIn('calibration_delta_pct', acc_data)

    def test_officer_portal_and_auth_endpoints(self):
        # Auth me
        me_res = self.client.get('/api/auth/me/')
        self.assertEqual(me_res.status_code, 200)
        self.assertIn('username', me_res.json())

        # Officer farmers list
        farmers_res = self.client.get('/api/officer/farmers/')
        self.assertEqual(farmers_res.status_code, 200)
        self.assertGreaterEqual(len(farmers_res.json()), 1)

        # Officer farmer detail
        farmer_detail_res = self.client.get(f'/api/officer/farmers/{self.farmer.id}/')
        self.assertEqual(farmer_detail_res.status_code, 200)
        self.assertEqual(farmer_detail_res.json()['username'], 'api_farmer')

    def test_alerts_and_messaging_endpoints(self):
        # Create alert
        alert_res = self.client.post('/api/alerts/', {
            'recipient': self.user.id,
            'field': self.field.id,
            'alert_type': 'PEST_OUTBREAK',
            'severity': 'HIGH',
            'title': 'Yellow Stem Borer Alert',
            'message': 'High humidity detected. Inspect field immediately.'
        }, format='json')
        self.assertEqual(alert_res.status_code, 201)
        alert_id = alert_res.json()['id']

        # List alerts
        list_alerts = self.client.get('/api/alerts/')
        self.assertEqual(list_alerts.status_code, 200)

        # Mark read
        read_res = self.client.patch(f'/api/alerts/{alert_id}/read/')
        self.assertEqual(read_res.status_code, 200)

        # Create conversation and message
        from apps.accounts.models import OfficerProfile
        officer_user = User.objects.create_user(username='test_officer', role=User.Role.OFFICER)
        officer = OfficerProfile.objects.create(user=officer_user)
        from apps.messaging.models import Conversation
        conv = Conversation.objects.create(farmer=self.farmer, officer=officer)

        # Send message
        msg_res = self.client.post(f'/api/messaging/conversations/{conv.id}/messages/', {
            'text_content': 'Hello Officer, how is the pest situation?',
            'type': 'text'
        }, format='json')
        self.assertEqual(msg_res.status_code, 201)

        # List messages
        msgs_res = self.client.get(f'/api/messaging/conversations/{conv.id}/messages/')
        self.assertEqual(msgs_res.status_code, 200)
        self.assertEqual(len(msgs_res.json()), 1)

