from django import forms

from .models import PrivateOffice, User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username', 'password']


class PrivateOfficeForm(forms.ModelForm):
    class Meta:
        model = PrivateOffice
        fields = ['mail_login', 'mail_password_imap', 'gmail_login', 'gmail_password_imap', 'yandex_login', 'yandex_pssword_imap']
