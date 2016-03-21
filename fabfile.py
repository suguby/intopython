# -*- coding: utf-8 -*-
import sys

import django
from django.conf import settings as django_settings
from fabric.context_managers import cd
from fabric.operations import os, run, local
from fabric.state import env
from fabric.utils import abort
from fabric.main import list_commands as _list_commands

from src.fab.utils import _set_env, _message_ok
from src.fab.mysql import db_dump, db_load, db_get_from_remote, db_truncate, db_reinit


def _set_virtualenv_root():
    fab_path = sys.argv[0]
    bin_path = os.path.split(fab_path)[0]
    env.virtualenv_root = os.path.split(bin_path)[0]


def _set_vars_from_django_settings():
    u"""Окружение для указанного сервера"""
    env.db_name = django_settings.DATABASES['default']['NAME']
    env.DATABASENAME = env.db_name
    env.db_user = django_settings.DATABASES['default']['USER']
    env.db_password = django_settings.DATABASES['default']['PASSWORD']
    env.db_dump_file = '{project_root}/extra/{db_name}.sql'.format(**env)


def remote_run(server=None, command=None, param1='', param2='', param3=''):
    u"""Запуск fab-команды на удалённом сервере, можно указать до 3-х параметров"""
    if server is None or command is None:
        abort("Укажите имя сервера и команду !!!")
    _set_env(server)  # Инициализация окружения
    params = ''
    params += ':{}'.format(param1) if param1 else ''
    params += ',{}'.format(param2) if param2 else ''
    params += ',{}'.format(param3) if param3 else ''
    command = 'bin/fab.sh {}{}'.format(command, params)
    with cd(env.project_root):  # Заходим в директорию с проектом на сервере
        run('{}'.format(command))


def get_settings_vars():
    u"""хелпер для определения значений переменных в сеттингах"""
    for var in ('MYSQL_DUMPS_PATH', ):
        print('{}={}'.format(var, getattr(django_settings, var)))
    print('DATABASENAME={}'.format(env.db_name))
    sys.exit(0)


def completion():
    u"""хелпер для автокомплита fab-команд"""
    print(' '.join(_list_commands('', 'short')), end='')
    sys.exit(0)


def pygments_css(schema='colorful'):
    if schema=='list':
        from pygments.styles import get_all_styles
        _message_ok('Avalible styles: {}'.format(', '.join(list(get_all_styles()))))
    else:
        local("pygmentize -f html -S {schema} -a .codehilite > {static_root}/css/pygments.css".format(
            static_root=django_settings.STATIC_ROOT,
            schema=schema,
        ))

django.setup()

env.project_root = django_settings.BASE_DIR
env.all_questions_yes = False
env.colorize_errors = True  # для красоты
env.use_ssh_config = True  # позволяет коннектится по алиасам из
_set_virtualenv_root()
_set_vars_from_django_settings()


# pycharm import import stub
stub = (
    db_dump, db_load, db_get_from_remote, db_truncate, db_reinit,
)
