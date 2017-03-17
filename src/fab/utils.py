# -*- coding: utf-8 -*-
import inspect
import os
import re
from tempfile import NamedTemporaryFile as _NamedTemporaryFile
from django.conf import settings as django_settings
from fabric.colors import green, yellow
from fabric.context_managers import cd
from fabric.operations import prompt, local, run
from fabric.state import env
from fabric.tasks import get_task_details
from fabric.utils import abort, puts

from src.common.utils import limit_str


def _ask(mess, exit_if_no=False, default='y'):
    try:
        if env.all_questions_yes:
            return True
    except AttributeError:
        pass
    answer = prompt(mess + ' (Y/n/a/q)', default=default, validate='[yYnNaAqQ]')
    if answer in 'yY':
        return True
    if answer in 'aA':
        env.all_questions_yes = True
        return True
    if answer in 'nN':
        if exit_if_no:
            abort('Canceled')
        return False
    if answer in 'qQ':
        abort('Canceled')


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
    _set_project_depended_vars(project_root=server_params['project_root'])
    env.shell = '/bin/bash -c'  # Используем шелл отличный от умолчательного (на сервере)
    env.use_ssh_config = True  # позволяет коннектится по алиасам из конфига


def _set_project_depended_vars(project_root):
    env.project_root = project_root
    env.python = os.path.join('env', 'bin', 'python')
    env.pip = os.path.join('env', 'bin', 'pip')
    env.requirements = os.path.join('requirements.txt')
    env.manage = os.environ['MANAGE_SH']  # TODO упростить


def _show_log(log_file, less=''):
    if less:
        local('less {}'.format(log_file))
    else:
        _message_warn('To stop tailing log press Ctrl-C')
        local('tail -f {}'.format(log_file))


def _fill_constants_from_settings(file_from, file_to):
    pattern = re.compile(r'##(?P<constant>[a-zA-Z_]*)##')
    with open(file_from, 'r') as fr:
        template = fr.read()
        while True:
            match = pattern.search(template)
            if not match:
                break
            constant = match.group('constant')
            constant_value = None
            try:
                constant_value = getattr(django_settings, constant)
            except AttributeError:
                try:
                    constant_value = getattr(env, constant)
                except AttributeError:
                    abort('No constant {} in Django settings or fabric env! '
                          'Found in {} file.'.format(constant, file_from))
            template = template.replace('##{}##'.format(constant), str(constant_value))
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


def _get_settings_var_from_remote(var_name):
    with cd(env.project_root):
        output = run('bin/fab.sh get_settings_vars', quiet=True)
        remote_var_value = None
        for line in output.split('\n'):
            var, val = line.split('=')
            if var == var_name:
                remote_var_value = val.strip()
    if not remote_var_value:
        abort("Не могу определить {} на сервере!!!".format(var_name))
    _message_ok('remote {}={}'.format(var_name, remote_var_value))
    return remote_var_value


def _remote_path_exists(path):
    with cd(env.project_root):
        output = run('bin/fab.sh dump_file_exists:{}'.format(path), quiet=True)
        return 'True' in output


def notified(wrapped):

    def internal(*args, **kwargs):
        res = wrapped(*args, **kwargs)
        params = list(args)
        params.extend([u'{}={}'.format(k, v) for k, v in kwargs.items()])
        params = [limit_str(p) for p in params]
        message = "{}({}) ended!!!".format(wrapped.__name__, ', '.join(params))
        _notify(message)
        return res

    def _details():
        return get_task_details(wrapped)

    internal.__doc__ = wrapped.__doc__
    internal.__details__ = _details
    return internal


def _notify(message):
    if hasattr(django_settings, 'FAB_NOTIFY_TASK_ENDS') and django_settings.FAB_NOTIFY_TASK_ENDS:
        local(u'notify-send --expire-time=10000 --icon=alarm-clock "Fabric notify" "{}"'.format(message), capture=True)
