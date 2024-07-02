from django.db import models

from users.models import User

class MessagesFromEmail(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="messages")
    message_subject = models.CharField(max_length=200)
    message_from = models.CharField(max_length=200)
    message_from_email = models.CharField(max_length=200)
    message_text = models.TextField()
    attachments = models.CharField(max_length=300, blank=True, null=True)
    message_date_recieve = models.DateTimeField()


# class Attachments(models.Model):
#     message = models.ForeignKey(MessagesFromEmail, related_name='attachments', on_delete=models.CASCADE)
#     file = models.FileField(upload_to='uploads/')