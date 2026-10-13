from apps.alerts.models import Alert
from apps.data_layer.models import Field
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging

logger = logging.getLogger(__name__)

def generate_alerts_from_coordination(field: Field, coordination_result: dict, sender=None) -> list:
    """
    Evaluates coordination risk flags and agent outputs to automatically generate
    and broadcast alerts to the field owner.
    """
    created_alerts = []
    recipient = field.owner.user if field.owner and field.owner.user else None
    if not recipient:
        return created_alerts

    risk_flags = coordination_result.get('risk_flags', [])
    agent_outputs = coordination_result.get('agent_outputs', {})
    channel_layer = get_channel_layer()

    # 1. Evaluate Pest & Disease Risks
    pest_out = agent_outputs.get('pest', {})
    if pest_out.get('risk_category') == 'high' or pest_out.get('pest_risk_score', 0) >= 0.7:
        alert = Alert.objects.create(
            sender=sender,
            recipient=recipient,
            field=field,
            alert_type='PEST_OUTBREAK',
            severity='HIGH',
            title=f"Elevated Pest Risk: {field.crop_type.capitalize()}",
            message=pest_out.get('reason', 'Favorable microclimate for pest/pathogen outbreak detected.')
        )
        created_alerts.append(alert)

    # 2. Evaluate Weather & Thermal Extremes
    weather_out = agent_outputs.get('weather', {})
    if weather_out.get('temp_risk_level') == 'high' or weather_out.get('extreme_event_risk', False):
        alert = Alert.objects.create(
            sender=sender,
            recipient=recipient,
            field=field,
            alert_type='EXTREME_WEATHER',
            severity='HIGH',
            title="Extreme Agrometeorological Warning",
            message=weather_out.get('reason', 'Critical thermal or precipitation anomaly projected.')
        )
        created_alerts.append(alert)

    # 3. Broadcast created alerts via WebSocket channel layer
    if channel_layer:
        for alert in created_alerts:
            try:
                async_to_sync(channel_layer.group_send)(
                    f'alerts_{recipient.id}',
                    {
                        'type': 'alert_notification',
                        'id': alert.id,
                        'alert_type': alert.alert_type,
                        'severity': alert.severity,
                        'title': alert.title,
                        'message': alert.message,
                        'field_id': field.id,
                        'timestamp': alert.created_at.isoformat()
                    }
                )
            except Exception as e:
                logger.warning("Could not dispatch WebSocket alert: %s", str(e))

    return created_alerts
