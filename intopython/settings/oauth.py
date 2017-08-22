# -*- coding: utf-8 -*-

# import social_core.backends.yandex


AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.vk.VKOAuth2',
    # 'social_core.backends.github.GithubOAuth2',  # TODO обработка нет емейла от сервиса
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.yandex.YandexOAuth2',

    # 'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.twitter.TwitterBackend',
    # 'social_core.backends.yandex.YandexOAuth2Backend',
    # 'social_core.backends.mailru.MailruBackend',

    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_SCOPE = ['email']
SOCIAL_AUTH_USER_FIELDS = ['email']


# http://python-social-auth.readthedocs.io/en/latest/backends/facebook.html
SOCIAL_AUTH_FACEBOOK_KEY = '...'
SOCIAL_AUTH_FACEBOOK_SECRET = '...'
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#     'locale': 'ru_RU',
#     'fields': 'email'
# }
#SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.9'


# http://python-social-auth.readthedocs.io/en/latest/backends/vk.html
SOCIAL_AUTH_VK_OAUTH2_KEY = ''
SOCIAL_AUTH_VK_OAUTH2_SECRET = ''

# http://python-social-auth.readthedocs.io/en/latest/backends/github.html
SOCIAL_AUTH_GITHUB_KEY = '...'
SOCIAL_AUTH_GITHUB_SECRET = '...'
# Для проды обновить Authorization callback URL !!!

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '...'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '...'

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = '...'
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = '...'
SOCIAL_AUTH_YANDEX_OAUTH2_SCOPE = ['login:email']
# https://tech.yandex.ru/oauth/doc/dg/reference/web-client-docpage/

try:
    from .local_oauth import *
except ImportError:
    print("Can't find module settings.local_oauth! Make it from local_oauth.py.skeleton")
