from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('send_login_email', views.send_login_email, name='send_login_email'),
]