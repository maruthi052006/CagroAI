import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlertConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer delivering real-time agrometeorological and pest alerts
    directly to a farmer or agri-officer's private channel (alerts_<user_id>).
    """
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'alerts_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def alert_notification(self, event):
        """
        Receives an alert event from channel_layer and sends JSON payload to client.
        """
        await self.send(text_data=json.dumps({
            'id': event.get('id'),
            'alert_type': event.get('alert_type'),
            'severity': event.get('severity'),
            'title': event.get('title'),
            'message': event.get('message'),
            'field_id': event.get('field_id'),
            'timestamp': event.get('timestamp')
        }))
