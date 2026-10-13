from apps.data_layer.models import Field, PredictionLog, FieldRecord
from apps.data_layer.nasa_client import NASAPowerClient
from apps.agents.agents import CropGrowthAgent, WeatherAgent, PestDiseaseAgent, YieldForecastAgent
from apps.coordination.resolver import resolve_outputs
from apps.coordination.trust_score import compute_trust_score
from apps.coordination.farm_health import compute_farm_health_index
from apps.agent_chat.models import AgentConversation, AgentChatMessage, Persona
from apps.agent_chat.intent_classifier import classifier
from apps.agent_chat.response_templates import render_response

def get_or_generate_field_context(field: Field) -> dict:
    """
    Retrieves latest stored PredictionLog or computes a fresh real grounded
    prediction context if no prior log exists.
    """
    latest_log = PredictionLog.objects.filter(field=field).order_by('-timestamp').first()
    if latest_log and isinstance(latest_log.output_data, dict):
        data = dict(latest_log.output_data)
        data['crop_type'] = field.crop_type
        return data

    # Pull latest record or fallback to NASA Power client
    latest_rec = FieldRecord.objects.filter(field=field).order_by('-date').first()
    if latest_rec:
        temp = latest_rec.temperature or 28.0
        moisture = latest_rec.soil_moisture or 55.0
        humidity = latest_rec.humidity or 65.0
        rainfall = latest_rec.rainfall or 10.0
        src = "REAL"
    else:
        nasa = NASAPowerClient()
        weather = nasa.fetch_weather(field.latitude, field.longitude)
        temp = weather['temperature']
        moisture = 55.0
        humidity = weather['humidity']
        rainfall = weather['rainfall']
        src = weather.get('source', 'EXTERNAL_NASA_POWER')

    field_data = {
        'crop_type': field.crop_type,
        'temperature': temp,
        'soil_moisture': moisture,
        'humidity': humidity,
        'rainfall': rainfall,
        'source': src
    }

    agent_outputs = {
        'crop_growth': CropGrowthAgent().run(field_data),
        'weather': WeatherAgent().run(field_data),
        'pest': PestDiseaseAgent().run(field_data),
        'yield': YieldForecastAgent().run(field_data)
    }

    resolved = resolve_outputs(agent_outputs, field_data)
    trust = compute_trust_score(agent_outputs, field, resolved, field_data)
    health = compute_farm_health_index(agent_outputs, field_data)

    context = {
        'crop_type': field.crop_type,
        'agent_outputs': agent_outputs,
        'conflicts_detected': resolved.get('conflicts_detected', []),
        'final_recommendation': resolved.get('final_recommendation', 'Maintain routine operations.'),
        'reasoning_trace': resolved.get('reasoning_trace', []),
        'trust_score': trust,
        'farm_health_index': health,
        'risk_flags': resolved.get('risk_flags', [])
    }

    # Cache as PredictionLog
    PredictionLog.objects.create(field=field, output_data=context)
    return context


def handle_agent_chat(field_id: int, persona_str: str, message_text: str) -> dict:
    """
    Main entry point for agent and EXAI conversation.
    Strictly zero external LLM. Uses 100% project-internal data & templates.
    """
    field = Field.objects.filter(id=field_id).first()
    if not field:
        # Fallback to demo field
        field = Field.objects.first()
        if not field:
            raise ValueError(f"Field with ID {field_id} not found and no demo field exists.")

    # Normalize persona
    persona_upper = persona_str.upper()
    valid_personas = [p.value for p in Persona]
    if persona_upper not in valid_personas:
        persona_upper = Persona.EXAI

    # Retrieve or create conversation
    conversation, _ = AgentConversation.objects.get_or_create(
        field=field,
        persona=persona_upper
    )

    # 1. Record User Message
    AgentChatMessage.objects.create(
        conversation=conversation,
        sender=AgentChatMessage.SenderRole.USER,
        text=message_text
    )

    # 2. Local Intent Classification
    intent, confidence = classifier.classify(persona_upper, message_text)

    # 3. Context Grounding
    context = get_or_generate_field_context(field)

    # 4. Template-Based Natural Language Generation
    reply_text, data_sources = render_response(persona_upper, intent, context)

    # 5. Record and Return Agent Response
    agent_msg = AgentChatMessage.objects.create(
        conversation=conversation,
        sender=AgentChatMessage.SenderRole.AGENT,
        intent_detected=intent,
        text=reply_text,
        data_sources_used=data_sources
    )

    return {
        "conversation_id": conversation.id,
        "persona": persona_upper,
        "intent": intent,
        "confidence": confidence,
        "reply": reply_text,
        "data_sources_used": data_sources,
        "created_at": agent_msg.created_at.isoformat()
    }
