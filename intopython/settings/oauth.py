# -*- coding: utf-8 -*-

from social_core.backends.facebook import FacebookOAuth2

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    # 'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.vkontakte.',
    # 'social_core.backends.facebook.FacebookBackend',
    # 'social_core.backends.google.GoogleOAuth2Backend',
    # 'social_core.backends.twitter.TwitterBackend',
    # 'social_core.backends.yandex.YandexOAuth2Backend',
    # 'social_core.backends.mailru.MailruBackend',

    'django.contrib.auth.backends.ModelBackend',
)

# http://python-social-auth.readthedocs.io/en/latest/backends/facebook.html
SOCIAL_AUTH_FACEBOOK_KEY = '...'
SOCIAL_AUTH_FACEBOOK_SECRET = '...'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_USER_FIELDS = ['email']
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#     'locale': 'ru_RU',
#     'fields': 'email'
# }

try:
    from .local_oauth import *
except ImportError:
    print("Can't find module settings.local_oauth! Make it from local_oauth.py.skeleton")
