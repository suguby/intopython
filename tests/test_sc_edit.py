# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from src.screencasts.models import Screencast, ScreencastSection
from src.screencasts.views import ScreencastCreateView, ScreencastEditView


class TestScreencastsEdit(TestCase):

    def setUp(self):
        UserModel = get_user_model()
        self.user_email = 'test@test.ru'
        self.user_password = '123'
        self.user = UserModel.objects.create_user(email=self.user_email, password=self.user_password)

        self.admin_email = 'admin@test.ru'
        self.admin_password = '321'
        self.admin = UserModel.objects.create_user(email=self.admin_email, password=self.admin_password)
        self.admin.is_admin = True
        self.admin.save()

        self.section = ScreencastSection.objects.create(title='test')

        self.exists_sc = Screencast.objects.create(
            section=self.section,
            video='<iframe width="560" height="315" src="" frameborder="0" allowfullscreen>pro video</iframe>',
            title='SC by_subscription',
            by_subscription=True,
            body='PRO ONLY',
            status=Screencast.STATUSES.publ,
        )
        self.exists_sc_edit_url = reverse('screencast_edit', kwargs=dict(slug=self.exists_sc.slug))

    def test_new_by_anonymous(self):
        response = self.client.get(reverse('screencast_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_new_by_usual_user(self):
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(reverse('screencast_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_new_by_admin(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.get(reverse('screencast_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ScreencastCreateView.title)

    def test_new_by_admin_post(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.post(
            reverse('screencast_add'),
            data=dict(
                title='test sc',
                section=self.section.id,
                video='test_video',
                body='bla-bla',
                status="draft",
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('screencasts'), response.url)
        sc = Screencast.objects.get(slug='test-sc')
        self.assertEqual(sc.title, 'test sc')
        self.assertEqual(sc.section, self.section)
        self.assertEqual(sc.video, 'test_video')
        self.assertEqual(sc.body, 'bla-bla')
        self.assertEqual(sc.status, "draft")

    def test_edit_by_anonymous(self):
        response = self.client.get(self.exists_sc_edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_edit_by_usual_user(self):
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(self.exists_sc_edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_edit_by_admin(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.get(self.exists_sc_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ScreencastEditView.title)

    def test_new_by_admin_post(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.post(
            self.exists_sc_edit_url,
            data=dict(
                title=self.exists_sc.title,
                section=self.section.id,
                video='test_video',
                body='bla-bla',
                status="draft",
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('screencast_detail', kwargs=dict(slug=self.exists_sc.slug)), response.url)
        sc = Screencast.objects.get(slug=self.exists_sc.slug)
        self.assertEqual(sc.section, self.section)
        self.assertEqual(sc.video, 'test_video')
        self.assertEqual(sc.body, 'bla-bla')
        self.assertEqual(sc.status, "draft")

