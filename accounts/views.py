from .models import Token
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import auth


def send_login_email(request):
    """отправить сообщение для входа в систему"""
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri( # применяется в Django для создания «полного» URL-адреса, включая доменное имя и часть с http(s)
        reverse('login') + '?token=' + str(token.uid)
    )
    send_mail(
        'Ваша ссылка для доступа к списку дел',
        f'Используйте эту ссылку для входа: {url}',
        'noreply@superlists',
        [email],
    )
    messages.add_message( # инфраструктура сообщений предоставляет более одного способа достигнуть того же результата
        request,
        messages.SUCCESS,
        "Проверьте свою почту. В сообщении находится ссылка, которая позволит войти на сайт."
    )
    return redirect('/')


def login(request):
    """зарегистрировать пользователя в системе"""
    token = request.GET.get('token')
    user = auth.authenticate(uid=token)
    auth.login(request, user)
    return redirect('/')
