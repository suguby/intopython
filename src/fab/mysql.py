# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import call_command
from fabric.context_managers import lcd, cd
from fabric.operations import local, os, run, get
from fabric.state import env
from fabric.utils import abort

from src.common.utils import dt
from src.fab.utils import _ask, _message_ok, _fill_and_save, _set_env, _get_settings_var_from_remote, notified, \
    _message_warn, _remote_path_exists


def _truncate_db():
    temp_sql_file = '{project_root}/extra/recreate_db.sql'.format(**env)
    template_file = '{project_root}/etc/recreate_db.sql.skeleton'.format(**env)
    _fill_and_save(template_file, temp_sql_file)
    local(_mysql_command() + ' < ' + temp_sql_file)
    local('rm -f ' + temp_sql_file)


def db_truncate():
    u"""Очистить БД """
    if _ask('Вы уверены что хотите очистить БД {db_name}?'.format(**env), exit_if_no=True):  # здесь нельзя юникод
        _truncate_db()


def db_reinit(username='wad'):
    u"""Пересоздать БД, накатить миграции, создать суперпользователя"""

    if _ask('Вы уверены что хотите пересоздать БД {db_name}?'.format(**env), exit_if_no=True):  # здесь нельзя юникод
        _truncate_db()
        call_command('migrate')
        _message_ok('Enter superuser {username} password', username=username)
        call_command('createsuperuser', username=username, email='user@domain.ru', noinput=1)
        _message_ok('Current {db_name} database purged', db_name=env.db_name)


def _get_dump_file_name(date=None, postfix='', dump_path='', db_name='', makepath=True):
    if date:
        if isinstance(date, str):
            date = dt(date)
    if not dump_path:
        dump_path = django_settings.MYSQL_DUMPS_PATH
    if date:
        dump_path = os.path.join(dump_path, date.strftime('%Y/%m/%d'))
    if makepath and not os.path.exists(dump_path):
        local('mkdir -p {}'.format(dump_path))
    file_name = db_name if db_name else env.db_name
    if postfix:
        file_name += '__' + postfix
    file_name += '.sql.gz'
    return os.path.join(dump_path, file_name)


def db_dump(date='', nodata='', ):
    u"""Выгрузить базу MySQL, только структуру если nodata='nodata' """
    options = '--no-data' if nodata else ''
    dump_file_name = _get_dump_file_name(date=date, postfix='nodata' if nodata else '')
    command = '{} | gzip > {}'.format(_mysql_command(dump=True, options=options), dump_file_name)
    local(command)
    return dump_file_name


# def db_dump_essential(date=''):
#     u"""Выгрузить базу MySQL только с минимально необходимыми табличками"""
#     NO_NEED_TABLES = ('visits', 'hits', 'urls', 'statistics', 'client_params', 'key_phrases',
#                       'user_agent_params', 'goal_reaches', 'domains', 'conversion_data', 'adv_marks', 'geo_info',
#                       'orders', 'order_items')
#     dump_file_name = _get_dump_file_name(date=date, postfix='essential')
#     options = ' '.join(['--ignore-table={}.{}'.format(env.db_name, tbl) for tbl in NO_NEED_TABLES])
#     command = '{} | gzip > {}'.format(_mysql_command(dump=True, options=options), dump_file_name)
#     local(command)


def db_load(date='', postfix='', truncate='no', migrate='yes'):
    u"""Загрузить базу MySQL, postfix м.б. nodata / essential """
    if truncate == 'yes':
        _truncate_db()
    dump_file_name = _get_dump_file_name(date=date, postfix=postfix)
    command = 'gunzip --to-stdout {} | {} '.format(dump_file_name, _mysql_command())
    local(command)
    if migrate == 'yes':
        local('bin/manage.sh migrate')


# def db_load_essential(date='', truncate=''):
#     u"""Загрузить урезанную, но рабочую базу MySQL"""
#     if truncate:
#         _truncate_db()
#     db_load(date=date, postfix='nodata')
#     db_load(date=date, postfix='essential')
#     if truncate:
#         local('bin/manage.sh migrate')

class RemoteDbGetter(object):

    def __init__(self, date, overwrite=False):
        self.date = date
        self.overwrite = overwrite
        self.remote_dump_path = _get_settings_var_from_remote('MYSQL_DUMPS_PATH')
        self.remote_db_name = _get_settings_var_from_remote('DATABASENAME')

    def _do_remote_dump(self, postfix):
        fab_command = 'db_dump'
        if postfix == 'essential':
            fab_command += '_essential'
        fab_command += ':{}'.format(self.date)
        if postfix == 'nodata':
            fab_command += ',nodata'
        with cd(env.project_root):
            run('bin/fab.sh {}'.format(fab_command))

    def get(self, postfix='', migrate='yes'):
        remote_file = _get_dump_file_name(
            date=self.date,
            postfix=postfix,
            dump_path=self.remote_dump_path,
            db_name=self.remote_db_name,
            makepath=False,
        )
        if self.overwrite or not _remote_path_exists(remote_file):
            self._do_remote_dump(postfix)
        local_file = _get_dump_file_name(
            date=self.date,
            postfix=postfix,
        )
        get(remote_file, local_file)
        db_load(date=self.date, postfix=postfix, migrate=migrate)


@notified
def db_get_from_remote(server='', date='', full='', truncate='yes', overwrite='no', migrate='yes'):
    u"""Загрузить урезанную, но рабочую базу MySQL c удаленного сервера"""
    if not server:
        abort("Укажите имя сервера!!!")
    if truncate == 'yes':
        _truncate_db()
    _set_env(server)
    db_getter = RemoteDbGetter(date, overwrite=(overwrite == 'yes'))
    if full:
        db_getter.get(migrate=migrate)
    else:
        db_getter.get(postfix='nodata', migrate='no')
        db_getter.get(postfix='essential', migrate=migrate)


def _mysql_command(dump=False, options=''):
    params = dict(**env)
    if dump:
        params['command'] = 'mysqldump'
        params['options'] = "--verbose --opt --routines --triggers --max_allowed_packet=265Mb"
    else:
        params['command'] = 'mysql'
        params['options'] = "--max_allowed_packet=265Mb"
    if options:
        params['options'] += ' ' + options
    return '{command} -h localhost -u {db_user} -p{db_password} {options} {db_name}'.format(**params)