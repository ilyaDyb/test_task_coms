import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from main.models import MessagesFromEmail
from main.utils.read_messages import start_reading

from users.models import User


class MessageConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        print("WebSocket connection accepted")


    async def disconnect(self, close_code):
        print(f"WebSocket connection closed with code: {close_code}")


    async def receive(self, text_data):
        print(f"Message received: {text_data}")
        data = json.loads(text_data)
        user_id = data.get('user_id')
        resource = data.get('resource')

        req_user = await self.get_request_user(user_id=user_id)

        mail_pass, username = await self.get_mail_pass_username(user_id, resource)

        total_messages = await self.get_total_messages()

        await self.send(text_data=json.dumps({"total_messages": total_messages}))

        cnt = 0

        async for message in start_reading(mail_pass, username):
            if str(message) == "Emprty box":
                self.close(code=4000)
                break

            msg_model = await self.create_message_from_email(
                user=req_user,
                message_subject=message.get("title"),
                message_from=message.get("from_"),
                message_from_email=message.get("from_email"),
                message_text=message.get("text"),
                attachments=message.get("attachments"),
                message_date_recieve=message.get("date")
            )
            # print(message.get("attachments"))

            print(f"Message created: {msg_model}")

            
            # attachments = message.get("attachments", [])
            # if attachments:
            #     await self.save_attachments(msg_model, attachments)

            await self.send_message_to_client(msg_model)

            print(f"Message sent to client: {msg_model}")
            if cnt == total_messages:
                break
            cnt += 1
                

    @sync_to_async
    def get_mail_pass_username(self, user_id, resource):
        user = User.objects.get(pk=user_id)
        private_office = user.user_office
        if private_office:
            if resource == "mail":
                email_login = private_office.mail_login
                email_imap_password = private_office.mail_password_imap
            elif resource == "gmail":
                email_login = private_office.gmail_login
                email_imap_password = private_office.gmail_password_imap
            else:
                email_login = None
                email_imap_password = None
        else:
            email_login = None
            email_imap_password = None
        return email_imap_password, email_login
    
    @sync_to_async
    def get_total_messages(self):
        # Функция которая должна считать кол-во сообщений
        total_messages = 2
        return total_messages

    @sync_to_async
    def create_message_from_email(self, **kwargs):
        msg_model = MessagesFromEmail.objects.create(**kwargs)
        return msg_model
    
    async def send_message_to_client(self, msg_model):
        await self.send(text_data=json.dumps({
            "message_subject": msg_model.message_subject,
            "message_from": msg_model.message_from,
            "message_from_email": msg_model.message_from_email,
            "message_text": msg_model.message_text.replace("\n", "")[:400],
            "message_date_recieve": msg_model.message_date_recieve.isoformat(),
        }))
        print(f"Message sent to client: {msg_model}")
    
    @sync_to_async
    def get_request_user(self, user_id):
        return User.objects.get(id=user_id)
    
    # @sync_to_async
    # def save_attachments(self, message_instance, attachments):
    #     try:
    #         for filename, data in attachments:
    #             if filename:
    #                 attachment = Attachments(
    #                     message=message_instance
    #                 )
    #                 attachment.file.save(filename, ContentFile(data))
    #                 attachment.save()
    #     except ValueError:
    #         return