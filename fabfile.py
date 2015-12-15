# -*- coding: utf-8 -*-
from fabric.colors import green, yellow
from fabric.context_managers import cd
from fabric.operations import local, os, run
from fabric.state import env
from fabric.utils import puts, abort
from django.conf import settings as django_settings

env.all_questions_yes = False
env.colorize_errors = True  # для красоты
env.use_ssh_config = True  # позволяет коннектится по алиасам из конфига


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
    env.python = os.path.join(env.virtualenv_root, 'bin', 'python')
    env.pip = os.path.join(env.virtualenv_root, 'bin', 'pip')
    env.requirements = os.path.join('requirements', 'base.txt')
    env.manage = os.path.join('manage.py')
    env.shell = '/bin/bash -c'  # Используем шелл отличный от умолчательного (на сервере)
    env.use_ssh_config = True  # позволяет коннектится по алиасам из конфига


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
