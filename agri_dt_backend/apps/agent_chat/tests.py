import os
import re
import socket
import urllib.request
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from apps.data_layer.models import Field, PredictionLog
from apps.accounts.models import User, FarmerProfile
from apps.zones.models import Zone
from apps.agent_chat.intent_classifier import classifier
from apps.agent_chat.conversation_engine import handle_agent_chat

class AgentChatAndGuardrailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.zone = Zone.objects.create(name='Chat Zone', code='CHT', region_group='CENTRAL')
        self.user = User.objects.create_user(username='chat_farmer', role=User.Role.FARMER)
        self.farmer = FarmerProfile.objects.create(user=self.user, zone=self.zone)
        self.field = Field.objects.create(
            name='Chat Rice Plot',
            latitude=10.78,
            longitude=79.13,
            crop_type='rice',
            owner=self.farmer
        )

        # Seed sample PredictionLog with structured trace
        PredictionLog.objects.create(
            field=self.field,
            output_data={
                "crop_type": "rice",
                "final_recommendation": "Hold irrigation for 48 hours due to forecasted heavy precipitation.",
                "reasoning_trace": [
                    {"step": 1, "actor": "CropGrowthAgent", "statement": "Rice is at 45% vegetative stage.", "confidence": 0.88},
                    {"step": 2, "actor": "WeatherAgent", "statement": "35mm rainfall expected within 48h.", "confidence": 0.92},
                    {"step": 3, "actor": "ConflictDetector", "statement": "Irrigation request contradicts storm forecast.", "conflict": True},
                    {"step": 4, "actor": "Resolver", "statement": "Delayed irrigation to avoid soil waterlogging.", "final": True}
                ],
                "trust_score": {"trust_score": 88.0, "label": "High", "breakdown": {"agent_agreement": 36, "data_quality": 26, "historical_accuracy": 26}},
                "farm_health_index": {"score": 84.0, "rating": "OPTIMAL", "breakdown": {"crop_health": 85, "water_soil_health": 80, "pest_disease_health": 90, "climate_stability": 80}},
                "conflicts_detected": [{"issue": "irrigation_vs_rain", "description": "Rain forecast vs irrigation", "resolution": "Hold irrigation"}],
                "agent_outputs": {
                    "crop_growth": {"growth_stage": 45.0, "biomass_estimate": 1150.0, "confidence": 0.88, "reason": "Vegetative vigor index high."},
                    "weather": {"rain_forecast_7day": 35.0, "temp_risk_level": "medium", "reason": "Monsoon depression moving inland."},
                    "pest": {"pest_risk_score": 0.20, "risk_category": "low", "reason": "Humidity within manageable bounds."},
                    "yield": {"yield_mean": 4450.0, "yield_p10": 3950.0, "yield_p50": 4450.0, "yield_p90": 4850.0, "confidence": 0.90}
                }
            }
        )

    def test_no_external_llm_codebase_guardrail(self):
        """
        Permanent Guardrail Test: Scans backend and frontend for any imports or references
        to third-party LLM providers/SDKs or hosted LLM endpoints.
        Fails if any are discovered.
        """
        forbidden_tokens = [
            "openai", "anthropic", "google.generativeai", "cohere",
            "mistralai", "huggingface_hub", "langchain",
            "api.openai.com", "api.anthropic.com", "generativelanguage.googleapis.com"
        ]

        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        scanned_count = 0

        for root, dirs, files in os.walk(backend_dir):
            if any(p in root for p in [".git", "__pycache__", ".pytest_cache", "venv", ".venv", "site-packages"]):
                continue
            for file in files:
                if file.endswith((".py", ".js", ".jsx", ".json", ".html")):
                    if file == "tests.py" and "agent_chat" in root:
                        continue # allow self-reference in this test assertion
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().lower()
                    for token in forbidden_tokens:
                        if "." in token:
                            has_match = token in content
                        else:
                            has_match = bool(re.search(rf"\b{re.escape(token)}\b", content))
                        self.assertFalse(
                            has_match,
                            f"VIOLATION: Forbidden LLM token '{token}' discovered in {filepath}!"
                        )
                    scanned_count += 1

        self.assertGreater(scanned_count, 10, "Guardrail test must scan at least 10 project files.")

    def test_no_network_call_during_agent_chat_response(self):
        """
        Verifies that running agent chat across all personas does NOT make any HTTP/network calls.
        """
        personas_and_queries = [
            ("EXAI", "Why did you make this recommendation?"),
            ("CROP", "What is the current growth stage of my crop?"),
            ("WEATHER", "What is the 7-day rainfall forecast?"),
            ("PEST", "What is the current pest and disease risk level?"),
            ("YIELD", "What is the expected harvest yield?")
        ]

        def forbidden_connect(*args, **kwargs):
            raise AssertionError("Network socket connection attempted during agent chat execution!")

        with patch("socket.socket.connect", side_effect=forbidden_connect):
            for persona, query in personas_and_queries:
                res = handle_agent_chat(self.field.id, persona, query)
                self.assertIn("reply", res)
                self.assertIn("data_sources_used", res)
                self.assertGreater(len(res["data_sources_used"]), 0)

    def test_exai_why_question_walks_reasoning_trace(self):
        res = handle_agent_chat(self.field.id, "EXAI", "Why did you recommend this?")
        self.assertEqual(res["intent"], "WHY_QUESTION")
        self.assertIn("CropGrowthAgent", res["reply"])
        self.assertIn("WeatherAgent", res["reply"])
        self.assertIn("CoordinationLayer.reasoning_trace", res["data_sources_used"])

    def test_intent_classification_across_five_personas(self):
        intent_crop, _ = classifier.classify("CROP", "What is the vegetative growth stage?")
        self.assertEqual(intent_crop, "GROWTH_STATUS")

        intent_weather, _ = classifier.classify("WEATHER", "Is there flood rain risk this week?")
        self.assertEqual(intent_weather, "RAIN_RISK")

        intent_pest, _ = classifier.classify("PEST", "What is the pathogen disease risk level?")
        self.assertEqual(intent_pest, "PEST_RISK_LEVEL")

        intent_yield, _ = classifier.classify("YIELD", "What is the expected harvest kg/ha yield?")
        self.assertEqual(intent_yield, "YIELD_ESTIMATE")

        intent_exai, _ = classifier.classify("EXAI", "Explain my farm health score")
        self.assertEqual(intent_exai, "FARM_HEALTH_QUESTION")

    def test_clarification_intent_fallback(self):
        # Query out-of-domain for Crop agent
        res = handle_agent_chat(self.field.id, "CROP", "Can you book a flight ticket to Mumbai?")
        self.assertEqual(res["intent"], "CLARIFICATION")
        self.assertIn("I don't have that specific crop parameter", res["reply"])

    def test_agent_chat_api_endpoints(self):
        # Test personas list endpoint
        res_personas = self.client.get('/api/agent-chat/personas/')
        self.assertEqual(res_personas.status_code, 200)
        self.assertEqual(len(res_personas.json()), 5)

        # Test message post endpoint
        payload = {"field_id": self.field.id, "text": "What is the trust score?"}
        res_msg = self.client.post('/api/agent-chat/EXAI/message/', payload, format='json')
        self.assertEqual(res_msg.status_code, 200)
        data = res_msg.json()
        self.assertEqual(data["persona"], "EXAI")
        self.assertEqual(data["intent"], "TRUST_QUESTION")
        self.assertIn("trust score", data["reply"].lower())

        # Test history endpoint
        res_hist = self.client.get(f'/api/agent-chat/EXAI/history/?field_id={self.field.id}')
        self.assertEqual(res_hist.status_code, 200)
        self.assertGreaterEqual(len(res_hist.json()["messages"]), 2)

    def test_all_personas_intents_templates(self):
        # Crop templates
        res1 = handle_agent_chat(self.field.id, "CROP", "What is the estimated biomass accumulation?")
        self.assertIn("biomass", res1["reply"].lower())
        res2 = handle_agent_chat(self.field.id, "CROP", "What is your confidence score for the crop model?")
        self.assertIn("confidence", res2["reply"].lower())

        # Weather templates
        res3 = handle_agent_chat(self.field.id, "WEATHER", "What is the 7-day precipitation forecast?")
        self.assertIn("precipitation", res3["reply"].lower())
        res4 = handle_agent_chat(self.field.id, "WEATHER", "What is the temperature and thermal risk?")
        self.assertIn("thermal", res4["reply"].lower())

        # Pest templates
        res5 = handle_agent_chat(self.field.id, "PEST", "Why is the pest risk categorized this way?")
        self.assertIn("pest diagnostic", res5["reply"].lower())
        res6 = handle_agent_chat(self.field.id, "PEST", "Show historical pest outbreaks")
        self.assertIn("historical", res6["reply"].lower())

        # Yield templates
        res7 = handle_agent_chat(self.field.id, "YIELD", "What is the uncertainty range between P10 and P90?")
        self.assertIn("p10", res7["reply"].lower())
        res8 = handle_agent_chat(self.field.id, "YIELD", "Compare my yield with historical norms")
        self.assertIn("benchmark", res8["reply"].lower())

        # EXAI templates
        res9 = handle_agent_chat(self.field.id, "EXAI", "Were there any conflicts between the agents?")
        self.assertIn("conflict", res9["reply"].lower())
        res10 = handle_agent_chat(self.field.id, "EXAI", "What actionable recommendation should I take?")
        self.assertIn("recommendation", res10["reply"].lower())
        res11 = handle_agent_chat(self.field.id, "EXAI", "Explain my farm health index score")
        self.assertIn("farm health", res11["reply"].lower())
        res12 = handle_agent_chat(self.field.id, "EXAI", "Help me understand what you can do")
        self.assertIn("i am exai", res12["reply"].lower())

    def test_unlogged_field_generates_fresh_context(self):
        # Create a new field with no prior PredictionLog
        new_field = Field.objects.create(
            name='Fresh Maize Plot', latitude=11.5, longitude=78.2, crop_type='maize', owner=self.farmer
        )
        res = handle_agent_chat(new_field.id, "EXAI", "Why did you make this recommendation?")
        self.assertEqual(res["intent"], "WHY_QUESTION")
        self.assertIn("Maize", res["reply"])
        # Confirm a new PredictionLog was created
        self.assertTrue(PredictionLog.objects.filter(field=new_field).exists())
