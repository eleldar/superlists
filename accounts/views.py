from django.shortcuts import render, redirect
from django.core.mail import send_mail

def send_login_email(request):
    """отправить сообщение для входа в систему"""
    email = request.POST['email']
    send_mail(
        'Ваша ссылка для доступа к списку дел',
        'Используйте эту ссылку для входа:',
        'noreply@superlists',
        [email],
    )
    return redirect('/')
