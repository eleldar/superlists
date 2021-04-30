from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class Token(models.Model):
    """маркер"""
    email = models.EmailField()
    uid = models.CharField(max_length=255)


from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class ListUserManager(BaseUserManager):
    """Менеджер пользователя списка"""

    def create_user(self, email):
        """создать пользователя"""
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        """создать суперпользователя"""
        self.create_user(email)

class ListUser(AbstractBaseUser, PermissionsMixin):
    """пользователь списка"""
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email', 'height']

    objects = ListUserManager()

    @property
    def is_staff(self): # закомментированная строка
        return self.email == 'email@email.com' # жестко кодированным адресом электронной почты

    @property
    def is_active(self):
        return True

