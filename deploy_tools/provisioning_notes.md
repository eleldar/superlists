Обеспечение работы нового сайта
===============================
## Необходимые пакеты
* nginx
* Python 3.8.6
* virtualenv + pip
* Git

## Ubuntu:
* в файе ~/.profile добавить строку: alias python='/usr/bin/python3'
* sudo apt update
* sudo apt -y upgrade
* sudo apt install -y python-pip python-venv nginx

## Конфигурация виртуального узла Nginx
* в файле nginx.template.conf
* заменить SITENAME, например, на post-o-gram.com
## Служба Systemd
* в файле gunicorn-systemd.template.service
* заменить SITENAME, например, на на post-o-gram.com
* заменить SEKRIT почтовым паролем

## Структура папок:
/home/server
└── sites
    └── SITENAME
        ├── database
        ├── source
        │   ├── functional_tests
        │   ├── lists
        │   └── superlists
        ├── static
        │   └── bootstrap
        └── virtualenv
            ├── bin
            ├── include
            ├── lib
            ├── lib64 -> lib
            └── share

