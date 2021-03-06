# -*- coding: utf-8 -*-

"""intopython URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
# from django.conf import settings
# from django.conf.urls.static import static
from django.conf.urls.static import static
from django.contrib import admin

from intopython.views import IndexView

urlpatterns = [


    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^screencasts/', include('src.screencasts.urls')),
    url(r'^blog/', include('src.blog.urls')),
    url(r'^courses/', include('src.courses.urls')),
    url(r'^landing/', include('src.landing.urls')),

    url(r'^registration/', include('src.registration.urls')),
    url(r'^payments/', include('src.payments.urls')),

    url(r'^nimda/', include(admin.site.urls)),
    url(r'^markdownx/', include('markdownx.urls')),

    url('^social_oauth/', include('social_django.urls', namespace='social')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
