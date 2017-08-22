# -*- coding: utf-8 -*-
import os

from .base import BASE_DIR

LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE_NAME = os.path.join(LOG_DIR, 'intopython.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'standard': {
            'format': "%(asctime)s [%(levelname)s]: %(message)s",
            'datefmt': "%Y-%m-%d %I:%M:%S"
        },
        'console': {
            'format': "[%(levelname)s]: %(message)s",
            'datefmt': "%Y-%m-%d %I:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', ],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard',
        },
        'logfile': {
            'level': 'INFO',
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 20000000,
            'backupCount': 30,
            'filename': LOG_FILE_NAME,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'intopython_error': {
            'handlers': ['mail_admins', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile', ],
            'level': 'INFO',
        },
        'debug': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
    }
}

