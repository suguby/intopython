#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from src.screencasts.models import Screencast, ScreencastSection


class TestSubscription(TestCase):

    def setUp(self):
        self.user_email = 'test@test.ru'
        self.user_password = '123'
        UserModel = get_user_model()
        self.user = UserModel.objects.create_user(email=self.user_email, password=self.user_password)
        section = ScreencastSection.objects.create(title='test')
        self.sc_pro = Screencast.objects.create(
            section=section,
            video='<iframe width="560" height="315" src="" frameborder="0" allowfullscreen>pro video</iframe>',
            title='SC by_subscription',
            by_subscription=True,
            body='PRO ONLY',
            status=Screencast.STATUSES.publ,
        )
        self.sc_pro_detail = reverse('screencast_detail', kwargs=dict(slug=self.sc_pro.slug))

        self.sc_free = Screencast.objects.create(
            section=section,
            video='<iframe width="560" height="315" src="" frameborder="0" allowfullscreen>free video</iframe>',
            title='SC free',
            body='SC body text',
            status=Screencast.STATUSES.publ,
        )
        self.sc_list = reverse('screencasts')

    def test_sc_list_anonymous(self):
        response = self.client.get(self.sc_list)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'free video')
        self.assertNotContains(response, 'pro video')

    def test_sc_list_simple_user(self):
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(self.sc_list)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'free video')
        self.assertNotContains(response, 'pro video')

    def test_sc_list_subscribed_user(self):
        self.user.is_subscriber = True
        self.user.save()
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(self.sc_list)
        self.assertContains(response, 'free video')
        self.assertContains(response, 'pro video')

    def test_sc_detail_anonymous(self):
        response = self.client.get(self.sc_pro_detail)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Запрошенный вами материал доступен только в PRO версии.')

    def test_sc_detail_simple_user(self):
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(self.sc_pro_detail)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Запрошенный вами материал доступен только в PRO версии.')

    def test_sc_detail_subscribed_user(self):
        self.user.is_subscriber = True
        self.user.save()
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(self.sc_pro_detail)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.sc_pro.body)
