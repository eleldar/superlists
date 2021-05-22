from django.db import models
import uuid # модуль Python для генерации идентификаторов
from django.contrib.auth import models as auth_models, signals as auth_signals

auth_signals.user_logged_in.disconnect(auth_models.update_last_login)

class User(models.Model):
    """пользователь"""
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

class Token(models.Model):
    """модель маркера"""
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)
