from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import time
from .models import Ops, MyUser
from client.views import check_ping, q
# from superadmin.plugin.novaclient import nova
# from superadmin.plugin.get_tokens import getToken
from django.utils import timezone
# from portal.settings import OPS_ADMIN, OPS_IP, OPS_PASSWORD, OPS_PROJECT, OPS_TOKEN_EXPIRED
# from superadmin.plugin.neutronclient import neutron
# from channels.layers import get_channel_layer
# from channels.db import database_sync_to_async
# from channels.auth import login, logout, get_user
# import fileinput
# from datetime import datetime
# from datetime import timedelta

class adminConsumer(WebsocketConsumer):
    def connect(self):
        self.admin_name = self.scope['url_route']['kwargs']['admin_name']
        self.room_group_name = 'superadmin'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()        

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        while (1):
            if q.fetch_job(message).result != None:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': q.fetch_job(message).result,
                    }
                )
                break
            else:
                time.sleep(3)
        # if Ops.objects.get(ip=message.split('abcxyz')[0]):
        #     thread = check_ping(host=message.split('abcxyz')[0])
        #     if thread.run():
        #         ops = Ops.objects.get(ip=message.split('abcxyz')[0])
        #         user = MyUser.objects.get(username=message.split('abcxyz')[1])
        #         # user = MyUser.objects.get(username='admin')
        #         if user.token_id is None or not user.check_expired():
        #             user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
        #             user.token_id = getToken(ip=ops.ip, username=OPS_ADMIN, password=OPS_PASSWORD,
        #                                      project_name=OPS_PROJECT, user_domain_id='default',
        #                                      project_domain_id='default')
        #             user.save()
        #         connect = nova(ip=ops.ip, token_id=user.token_id, project_name=user.username, project_domain_id=ops.projectdomain)
        #         async_to_sync(self.channel_layer.group_send)(
        #             self.room_group_name,
        #             {
        #                 'type': 'chat_message',
        #                 'message': connect.list_images(),
        #                 'network': connect.list_flavor(),
        #                 'sshkey': connect.list_sshkey(),
        #             }
        #         )
        # else:
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.room_group_name,
        #         {
        #             'type': 'chat_message',
        #             'message': message,
        #         }
        #     )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        try:
            network = event['network']
            sshkey = event['sshkey']
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message,
                'network': network,
                'sshkey': sshkey,
            }))
        except:
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message,
            }))