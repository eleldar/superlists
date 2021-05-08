from django.db import models
import uuid # модуль Python для генерации идентификаторов

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
