from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

import uuid
import sys
from .models import Token

def send_login_email(request):
    """Выслать ссылку для входа на почту"""
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('сохранение uid', uid, 'для почты', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Ваша ссылка для доступа к списку дел',
        f'Используйте эту ссылку для входа:\n{url}',
        'noreply@superlists',
        [email],
    )
    return render(request, 'accounts/login_email_sent.html')

def login(request):
    """регистрация в системе"""
    print('просмотр входа в систему', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid) # вызывает инфраструктуру аутентификации Django,
                                 # которую конфигурируем с помощью индивидуализированного
                                 # серверного процессора аутентификации, работа которого заключается в
                                 # валидации uid и возврате пользователя с правильной электронной почтой
    if user is not None:
        auth_login(request, user)
    return redirect('/')

def logout(request):
    """выход из системы"""
    auth_logout(request)
    return redirect('/')
