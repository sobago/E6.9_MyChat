import datetime
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.new_group(self.room_name)

        await self.accept()

    @database_sync_to_async
    def new_group(self, room):
        # Функция для добавления комнаты в базу
        try:
            Room.objects.get(title=room)
        except ObjectDoesNotExist:
            Room.objects.create(title=room, creator=self.scope['user'])

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user'].username
        time = datetime.datetime.now().strftime('%H:%M:%S')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'time': time
            }
        )
        await self.write_msg_to_db(message)

    @database_sync_to_async
    def write_msg_to_db(self, message):
        # Функция для добавления сообщения в базу
        Message.objects.create(text=message, sender=self.scope['user'], chat=Room.objects.get(title=self.room_name))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = self.scope['user'].username
        time = datetime.datetime.now().strftime('%H:%M:%S')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'time': time,
        }))
