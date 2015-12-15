# -*- coding: utf-8 -*-
import re
from tempfile import NamedTemporaryFile as _NamedTemporaryFile

import sys
from fabric.colors import green, yellow
from fabric.context_managers import cd
from fabric.operations import local, os, run
from fabric.state import env
from fabric.utils import puts, abort
from django.conf import settings as django_settings
import django


def _set_virtualenv_root():
    fab_path = sys.argv[0]
    bin_path = os.path.split(fab_path)[0]
    env.virtualenv_root = os.path.split(bin_path)[0]


def _message_ok(txt, **kwargs):
    puts(green(txt.format(**kwargs)))


def _message_warn(txt, **kwargs):
    puts(yellow(txt.format(**kwargs)))


def _set_env(server):
    u"""Окружение для указанного сервера"""
    server_params = dict()
    try:
        server_params = django_settings.FAB_SERVERS[server]
    except AttributeError:
        abort("Не задан словарь FAB_SERVERS в настройках !!!")
    except KeyError:
        abort("Не указан сервер {} в FAB_SERVERS в настройках !!!".format(server))
    if 'host' not in server_params:
        abort("Для сервера {} в FAB_SERVERS не задано поле host !!! (может быть алиасом из .ssh/config)".format(server))
    env.host_string = server_params['host']
    if 'user' in server_params:
        env.host_string = '{user}@{host}'.format(user=server_params['user'], host=env.host_string)
    if 'port' in server_params:
        env.host_string = '{host}:{port}'.format(host=env.host_string, port=server_params['port'])

    env.project_root = server_params['project_root']
    if 'virtualenv_root' in server_params:
        env.virtualenv_root = server_params['virtualenv_root']
    else:
        env.virtualenv_root = os.path.join(server_params['project_root'], 'env')
    # env.python = os.path.join(env.virtualenv_root, 'bin', 'python')
    # env.pip = os.path.join(env.virtualenv_root, 'bin', 'pip')
    # env.requirements = os.path.join('requirements', 'base.txt')
    # env.manage = '{}/intopython/manage.py'.format(env.project_root)
    env.shell = '/bin/bash -c'  # Используем шелл отличный от умолчательного (на сервере)
    env.use_ssh_config = True  # позволяет коннектится по алиасам из конфига


def _fill_constants_from_settings(file_from, file_to):
    pattern = re.compile(r'##(?P<constant>[a-zA-Z_]*)##')
    with open(file_from, 'r') as fr:
        template = fr.read()
        while True:
            match = pattern.search(template)
            if not match:
                break
            constant = match.group('constant')
            if hasattr(django_settings, constant):
                value = getattr(django_settings, constant)
            elif hasattr(env, constant):
                value = getattr(env, constant)
            else:
                abort('No constant {} in Django settings or fabric env! Found in {} file.'.format(constant, file_from))
            template = template.replace('##{}##'.format(constant), str(value))
        if isinstance(file_to, str):
            with open(file_to, 'w') as fw:
                fw.write(template)
        else:
            file_to.write(template)


def _fill_and_save(file_from, file_to, as_root=False):
    with _NamedTemporaryFile() as ff:
        _fill_constants_from_settings(file_from, ff.name)
        command = 'cp {} {}'.format(ff.name, file_to)
        if as_root:
            local('sudo ' + command)
        else:
            local(command)
        _message_ok('File {} generated form {}'.format(file_to, file_from))


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


def make_apache_conf():
    conf_file_template = '{}/conf/intopython_ru.conf'.format(env.project_root)
    _fill_and_save(file_from=conf_file_template, file_to='/tmp/intopython_ru.conf')


django.setup()

env.project_root = django_settings.BASE_DIR
env.all_questions_yes = False
env.colorize_errors = True  # для красоты
env.use_ssh_config = True  # позволяет коннектится по алиасам из
_set_virtualenv_root()
