from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SketchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # grab the sketch_id from the URL
        self.sketch_id = self.scope['url_route']['kwargs']['sketch_id']
        # use a unique group name per sketch
        self.room_group_name = f"sketch_{self.sketch_id}"

        # join that group
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

    async def receive(self, text_data):
        # broadcast incoming draw data to everyone in the same sketch group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_draw',
                'text': text_data
            }
        )

    async def broadcast_draw(self, event):
        # send the draw data back to the WebSocket
        await self.send(text_data=event['text'])

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room']
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get("type") == "peer_id":
            # 🔄 Handle Peer ID sync broadcast
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast_peer_id",
                    "peer_id": data["peer_id"],
                    "user_id": data["user_id"]
                }
            )
        else:
            # 📡 Handle normal signaling messages (unchanged)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "signal_message",
                    "message": text_data
                }
            )

    async def signal_message(self, event):
        # 🔁 Send original signaling message to room
        await self.send(text_data=event["message"])

    async def broadcast_peer_id(self, event):
        # 🎯 Send peer ID update to everyone else in room
        await self.send(text_data=json.dumps({
            "type": "peer_id",
            "peer_id": event["peer_id"],
            "user_id": event["user_id"]
        }))
