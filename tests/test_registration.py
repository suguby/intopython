#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestRegistration(TestCase):

    def test_login(self):
        email = 'test@test.ru'
        password = '123'
        data = dict(email=email, password=password)
        response = self.client.post(reverse('login'), data=data)

