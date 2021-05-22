from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views # встроенное в Django представление выхода из системы; очищает сеанс пользователя сверху-вниз и переадресует его на страницу по нашему выбору
from . import views

urlpatterns = [
    path('send_login_email', views.send_login_email, name='send_login_email'),
    path('login', views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]
