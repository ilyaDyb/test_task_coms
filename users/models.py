from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    class Meta:
        verbose_name = "user"


class PrivateOffice(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="user_office")

    mail_login = models.EmailField(max_length=150, blank=True, null=True)
    mail_password_imap = models.CharField(max_length=200, blank=True, null=True)

    gmail_login = models.EmailField(max_length=150, blank=True, null=True)
    gmail_password_imap = models.CharField(max_length=200, blank=True, null=True)

    yandex_login = models.EmailField(max_length=150, blank=True, null=True)
    yandex_pssword_imap = models.CharField(max_length=200, blank=True, null=True)