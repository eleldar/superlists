from django.shortcuts import render, redirect
from django.core.mail import send_mail

def send_login_email(request):
    """отправить сообщение для входа в систему"""
    return redirect('/')
