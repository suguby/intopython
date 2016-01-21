# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from landing.models import LendingRegistration


class TestLanding(TestCase):

    def test_submit(self):
        data = dict(email='test@test.ru', name='тест', phone='12345')
        self.client.post(reverse('landing'), data=data)
        user = LendingRegistration.objects.get(email=data['email'])
        self.assertEquals(user.name, data['name'])

    def test_invalid_submit(self):
        data = dict(email='test@test', name='тест', phone='12345')
        self.client.post(reverse('landing'), data=data)
        queryset = LendingRegistration.objects.filter(email=data['email'])
        self.assertEquals(len(queryset), 0)

    def test_empty_submit(self):
        self.client.post(reverse('landing'), data=dict())
        queryset = LendingRegistration.objects.all()
        self.assertEquals(len(queryset), 0)
