# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from src.landing.models import LendingRegistration


class TestLanding(TestCase):

    def test_submit(self):
        data = dict(email='test@test.ru', name='тест', phone='12345')
        response = self.client.post(reverse('landing'), data=data)
        user = LendingRegistration.objects.get(email=data['email'])
        self.assertEquals(user.name, data['name'])
        self.assertTrue('show_thanks' in response.context_data)

    def test_invalid_submit(self):
        data = dict(email='test@test', name='тест', phone='12345')
        response = self.client.post(reverse('landing'), data=data)
        queryset = LendingRegistration.objects.filter(email=data['email'])
        self.assertEquals(len(queryset), 0)
        self.assertTrue('show_register' in response.context_data)

    def test_empty_submit(self):
        response = self.client.post(reverse('landing'), data=dict())
        queryset = LendingRegistration.objects.all()
        self.assertEquals(len(queryset), 0)
        self.assertTrue('show_register' in response.context_data)
