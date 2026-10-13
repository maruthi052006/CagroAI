import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from apps.accounts.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # TODO: Add JWT auth verification from scope here

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            message_text = text_data_json.get('message', '')
            user_id = text_data_json.get('user_id')
            msg_type = text_data_json.get('type', 'text')

            # Save to db
            msg = await self.save_message(user_id, self.conversation_id, message_text, msg_type)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_text,
                    'user_id': user_id,
                    'msg_type': msg_type,
                    'msg_id': msg.id if msg else None
                }
            )
            
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        msg_type = event['msg_type']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'type': msg_type,
            'status': 'delivered'
        }))

    @database_sync_to_async
    def save_message(self, user_id, conversation_id, text, msg_type):
        try:
            user = User.objects.get(id=user_id)
            conv = Conversation.objects.get(id=conversation_id)
            return Message.objects.create(
                conversation=conv,
                sender=user,
                text_content=text,
                type=msg_type
            )
        except (User.DoesNotExist, Conversation.DoesNotExist):
            return None
