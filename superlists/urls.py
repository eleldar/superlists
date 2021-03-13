"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from lists import views as list_views # хорошая практика назначать псевдонимы для высокоуровневого urls.py; 
from lists import urls as list_urls   # позволит, если нужно, импортировать представления и URL-адреса из многочисленных приложений

urlpatterns = [
    path('', list_views.home_page, name='home'),
    re_path(r'^lists/', include(list_urls)), # include может быть частью регулярного выражения в URL как префикс, 
                                             # который будет применяться ко всем включенным URL-адресам
]
