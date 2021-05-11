from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail

def send_login_email(request):
    """отправить сообщение для входа в систему"""
    email = request.POST['email']
    print(type(send_mail))
    send_mail(
        'Ваша ссылка для доступа к списку дел',
        'Используйте эту ссылку для входа:',
        'noreply@superlists',
        [email],
    )
    messages.add_message( # инфраструктура сообщений предоставляет более одного способа достигнуть того же результата
        request,
        messages.SUCCESS,
        "Проверьте свою почту. В сообщении находится ссылка, которая позволит войти на сайт."
    )
    return redirect('/')
