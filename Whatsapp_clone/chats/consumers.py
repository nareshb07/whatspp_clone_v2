import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import ChatModel ,UserProfileModel , ChatNotification, UserProfile
from .models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage



class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        
        my_id = self.scope['user'].id
        
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        receiver = data['receiver']
            
        #message_status = data[message_status]
            

        await self.save_message(username, self.room_group_name, message , receiver)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    @database_sync_to_async
    def save_message(self, username, thread_name, message,receiver):
        chat_obj = ChatModel.objects.create(
            sender=username, message=message, thread_name=thread_name)
        chat_obj.save()


        my_id = self.scope['user'].id
        receiver_id = self.scope['url_route']['kwargs']['id']

        try:

            UserProfile.objects.filter(Follower_id=my_id, user_id=receiver_id).update(message_seen=True)  
        except Exception as e:
            print(e) 

        try:
            u = UserProfile.objects.get(user_id = my_id, Follower_id = receiver_id  )
            u.last_message = timezone.now()
            u.save()
            u = UserProfile.objects.get(user_id = receiver_id, Follower_id = my_id   )
            u.last_message = timezone.now()
            u.save()
        except Exception as e:
            print(e)
        """
        other_user_id = self.scope['url_route']['kwargs']['id']
        get_user = User.objects.get(id=other_user_id)
        if receiver == get_user.username:
            ChatNotification.objects.create(chat=chat_obj, user=get_user)"""
    """
    async def handle_file_upload(self, bytes_data):
        # Process file upload
        file_name = 'uploaded_file.txt'  # You can modify the file name as per your requirements
        file_content = ContentFile(bytes_data)
        # Save the file to the desired location
        # For example, if you have a field named "file" in your ChatModel:
        chat_obj = ChatModel.objects.create(
            sender=self.scope['user'].username, message='', thread_name=self.room_group_name, file=file_content, file_name=file_name)
        chat_obj.save()""" 
    

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        self.room_group_name = f'{my_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
            
        )
        
        
        await self.accept()
    
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        print(count)
        await self.send(text_data=json.dumps({
            'count':count
        }))
        

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        print(connection_type)
        await self.change_online_status(username, connection_type)
    
    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']
        await self.send(text_data=json.dumps({
            'username':username,
            'online_status':online_status
        }))
    

    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    

    @database_sync_to_async
    
    def change_online_status(self, username, c_type):

        user = User.objects.get(first_name=username)
        try:
            
            userprofile = UserProfileModel.objects.get(user=user)
            if c_type == 'open':
                userprofile.online_status = True
                userprofile.save()
            else:
                userprofile.online_status = False
                userprofile.save()
        except Exception as e:
            print(e)
