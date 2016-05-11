#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from src.registration.models import MyUser


class TestRegistration(TestCase):

    def setUp(self):
        self.user_email = 'test@test.ru'
        self.user_password = '123'
        self.user = MyUser.objects.create_user(email=self.user_email, password=self.user_password)
        self.redirect_url = '/some'

    def test_login(self):
        data = dict(username=self.user_email, password=self.user_password)
        url = reverse('login') + '?next=' + self.redirect_url
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.redirect_url)

    def test_login_bad_credentials(self):
        data = dict(username='bla@bla.ru', password='bla-bla')
        url = reverse('login') + '?next=' + self.redirect_url
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пожалуйста, введите правильные адрес электронной почты и пароль')

