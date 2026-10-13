from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.agent_chat.models import AgentConversation, AgentChatMessage, Persona
from apps.agent_chat.conversation_engine import handle_agent_chat

class PersonasListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        personas = [
            {
                "id": "EXAI",
                "name": "EXAI Synthesizer",
                "title": "Explainable AI Persona",
                "description": "Synthesizes all 4 agents into clear, transparent reasoning traces, trust scores, and holistic farm health indices.",
                "icon": "Cpu",
                "accent_color": "#A855F7"
            },
            {
                "id": "CROP",
                "name": "CropGrowthAgent",
                "title": "Vegetative Dynamics Persona",
                "description": "Explains phenological stage progression, biomass accumulation, and thermal suitability index.",
                "icon": "Sprout",
                "accent_color": "#22C55E"
            },
            {
                "id": "WEATHER",
                "name": "WeatherAgent",
                "title": "Microclimate & Forecast Persona",
                "description": "Reports 7-day cumulative precipitation, heat stress risks, and precipitation hazard alerts.",
                "icon": "CloudSun",
                "accent_color": "#38BDF8"
            },
            {
                "id": "PEST",
                "name": "PestDiseaseAgent",
                "title": "Biosecurity & Pathology Persona",
                "description": "Analyzes pathogen pressure, humidity trigger thresholds, and TNAU integrated pest management advice.",
                "icon": "ShieldAlert",
                "accent_color": "#F43F5E"
            },
            {
                "id": "YIELD",
                "name": "YieldForecastAgent",
                "title": "Stochastic Yield Persona",
                "description": "Provides mean harvest projection (kg/ha) and 1,000-pass Monte Carlo P10-P90 uncertainty intervals.",
                "icon": "TrendingUp",
                "accent_color": "#EAB308"
            }
        ]
        return Response(personas)


class AgentChatMessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, persona):
        field_id = request.data.get('field_id')
        text = request.data.get('text', '').strip()

        if not text:
            return Response({"error": "Message text is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = handle_agent_chat(field_id=field_id, persona_str=persona, message_text=text)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AgentChatHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, persona):
        field_id = request.query_params.get('field_id')
        persona_upper = persona.upper()

        query = AgentConversation.objects.filter(persona=persona_upper)
        if field_id:
            query = query.filter(field_id=field_id)

        conversation = query.first()
        if not conversation:
            return Response({"messages": []})

        messages = conversation.messages.all().order_by('created_at')
        serialized = [
            {
                "id": m.id,
                "sender": m.sender,
                "intent": m.intent_detected,
                "text": m.text,
                "data_sources_used": m.data_sources_used,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]
        return Response({"conversation_id": conversation.id, "messages": serialized})
