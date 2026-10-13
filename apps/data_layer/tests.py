import datetime
from django.test import TestCase
from apps.data_layer.quality_engine import compute_data_quality
from apps.data_layer.nasa_client import NASAPowerClient
from apps.data_layer.models import Field, FieldRecord
from apps.accounts.models import User, FarmerProfile
from apps.zones.models import Zone

class DataLayerQualityEngineTests(TestCase):
    def test_clean_telemetry_quality(self):
        clean_data = {
            'crop_type': 'rice',
            'temperature': 27.5,
            'rainfall': 14.0,
            'humidity': 68.0,
            'soil_moisture': 62.0,
            'date': datetime.date.today().isoformat()
        }
        res = compute_data_quality(clean_data)
        self.assertGreaterEqual(res['quality_score'], 90.0)
        self.assertTrue(res['is_acceptable'])
        self.assertEqual(len(res['issues']), 0)

    def test_missing_fields_penalty(self):
        sparse_data = {
            'crop_type': 'wheat',
            'temperature': 22.0
            # missing rainfall, humidity, soil_moisture
        }
        res = compute_data_quality(sparse_data)
        self.assertLess(res['quality_score'], 80.0)
        self.assertTrue(any('Missing' in issue for issue in res['issues']))

    def test_outlier_detection(self):
        outlier_data = {
            'crop_type': 'cotton',
            'temperature': 68.0, # unphysical temp
            'rainfall': -15.0,   # negative rainfall
            'humidity': 120.0,   # unphysical humidity
            'soil_moisture': 140.0
        }
        res = compute_data_quality(outlier_data)
        self.assertLess(res['quality_score'], 40.0)
        self.assertFalse(res['is_acceptable'])
        self.assertTrue(any('Outlier' in issue for issue in res['issues']))
        self.assertTrue(any('Negative rainfall' in issue for issue in res['issues']))

    def test_staleness_penalty(self):
        stale_date = (datetime.date.today() - datetime.timedelta(days=20)).isoformat()
        stale_data = {
            'crop_type': 'groundnut',
            'temperature': 26.0,
            'rainfall': 5.0,
            'humidity': 55.0,
            'soil_moisture': 50.0,
            'date': stale_date
        }
        res = compute_data_quality(stale_data)
        self.assertLess(res['quality_score'], 90.0)
        self.assertTrue(any('staleness' in issue.lower() for issue in res['issues']))

    def test_nasa_client_fallback(self):
        client = NASAPowerClient()
        weather = client.fetch_weather(10.78, 79.13)
        self.assertIn('temperature', weather)
        self.assertIn('rainfall', weather)
        self.assertIn('humidity', weather)
        self.assertIn('source', weather)
        self.assertIn(weather['source'], ['EXTERNAL_NASA_POWER', 'EXTERNAL_FALLBACK'])
