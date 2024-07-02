from django.contrib import admin

from users.models import PrivateOffice, User

# Register your models here.
admin.site.register(User)
admin.site.register(PrivateOffice)