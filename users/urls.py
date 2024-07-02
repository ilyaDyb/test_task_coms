from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path('private_office/', views.private_office_view, name='private_office'),
]