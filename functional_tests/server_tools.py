from fabric.api import run
from fabric.context_managers import settings

def _get_manage_dot_py(host):
    '''получить строку адреса manage.py на сервере'''
    manage_dot_py = f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'
    return manage_dot_py

def reset_database(host, name='server'): # name - имя пользователя на сервере
    '''обнулить базу данных'''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{name}@{host}'): # установка имя узла с помощью контекстного менеджера
        run(f'{manage_dot_py} flush --noinput') # находясь в контекстном менеджере вызываем команды (в данном случае run), как будно находимся в fabfile.py

def create_session_on_server(host, email, name='server'): # name - имя пользователя на сервере
    '''создать сеанс на сервере'''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{name}@{host}'): # установка имя узла с помощью контекстного менеджера
        session_key = run(f'{manage_dot_py} create_session {email}') # находясь в контекстном менеджере вызываем команды (в данном случае run), как будно находимся в fabfile.py
        return session_key.strip()
