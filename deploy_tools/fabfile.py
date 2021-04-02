from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/eleldar/superlists.git'

def deploy():
    '''развернуть'''
    # env.host будет содержать адрес сервера, который передается в командной строке
    # env.user будет содержать имя пользователя, которое используется для входа на сервер
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    # Поскольку любая функция в fabfile теоретически может вызываться из командной строки,
    # то используется форма записи с начальным символом подчеркивания, которые указывают,
    # что они не предназначены быть частью общедоступного API в fabfile
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    '''создать структуру каталогов при необходимости'''
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}') # run для выполнения указанной команды оболочки на сервере
                                                   # mkdir -p создает указанную структуру папок при их отсутствии;
                                                   # если папки существуют, в т.ч. содержат файлы, то они сохраняются!

def _get_latest_source(source_folder):
    '''получить последнюю версию кода'''
    if exists(source_folder + '/.git'): # exists проверяет существование каталога или файла на сервере;
                                        # ищем папку .git, чтобы проверить, был ли репозиторий уже клонирован в нее
        run(f'cd {source_folder} && git fetch') # cd выполняет переход в текущий рабочий каталог на сервере (Fabric не помнит, в каком каталоге вы находитесь от одной команды run до другой)
                                                # git fetch внутри существующего репозитория получает все последние фиксации из веб (без немедленного обновления живого дерева исходного кода)
    else:
        run(f'git clone {REPO_URL} {source_folder}') # при отсутствии репозитория выполняем git clone с URL-адресом репозитория, чтобы принести свежее дерево исходного кода на сервер
    current_commit = local('git log -n 1 --format=%H', capture=True) # local (обертка для subprocess.Popen) используется дял получения ID текущей фиксации на локальной машине
    run(f'cd {source_folder} && git reset --hard {current_commit}') # стираем любые текущие изменения на сервере

def _update_settings(source_folder, site_name):
    '''обновить настройки'''
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False') # sed выполняет строковую замену в файле; здесь она меняет DEBUG с True на False
    sed(settings_path,
        'ALLOWED_HOSTS =.+$', # поиск совпадения с помощью регулярного выражения
        f'ALLOWED_HOSTS = ["{site_name}"]' # замена найденной строки
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file): # генерация нового ключа для его импорта в настройки при отсутствии файла (если есть секретный ключ, то он должен оставаться одинаковым между развертываниями)
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for item in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"') # append добавляет строку в конец файла
    append(settings_path, 'from .secret_key import SECRET_KEY')  # добавляем в конец файла settings.py ключ; при повторных разворачиваниях эта запись не добавляется, т.к. отменили все дейстия через git
                                                                 # используется относительный импорт (from .secret_key вместо from secret_key ),
                                                                 # чтобы быть абсолютно уверенным, что мы импортируем локальный модуль,
                                                                 # а не откуда-то в другом месте в sys.path

def _update_virtualenv(source_folder):
    '''обновить виртуальную среду'''
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'): # поиск внутри папки virtualenv исполняемого файла pip
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt') # обновление пакетов из файла requirements.txt

def _update_static_files(source_folder):
    '''обновить статические файлы'''
    # используем папку с двоичными файлами virtualenv для вызова команды manage.py, чтобы убедиться, что получаем virtualenv, а не системную версию
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput') 

def _update_database(source_folder):
    '''обновление базы данных'''
    # Опция --noinput удаляет любые интерактивные подтверждения в формате да/нет, с которыми Fabric не справляется
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')
