# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from src.blog.models import Blog
from src.blog.views import BlogCreateView, BlogEditView


class TestBlogEdit(TestCase):

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

        self.exists_blog = Blog.objects.create(
            title='Blog title',
            body='some text',
            status=Blog.STATUSES.publ,
        )
        self.exists_blog_edit_url = reverse('blog_edit', kwargs=dict(slug=self.exists_blog.slug))

    def test_new_by_anonymous(self):
        response = self.client.get(reverse('blog_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_new_by_usual_user(self):
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(reverse('blog_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_new_by_admin(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.get(reverse('blog_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BlogCreateView.title)

    def test_new_by_admin_post(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.post(
            reverse('blog_add'),
            data=dict(
                title='test blog',
                body='bla-bla',
                status="draft",
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('blog'), response.url)
        blog = Blog.objects.get(slug='test-blog')
        self.assertEqual(blog.title, 'test sc')
        self.assertEqual(blog.body, 'bla-bla')
        self.assertEqual(blog.status, "draft")

    def test_edit_by_anonymous(self):
        response = self.client.get(self.exists_blog_edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_edit_by_usual_user(self):
        self.client.login(username=self.user_email, password=self.user_password)
        response = self.client.get(self.exists_blog_edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_edit_by_admin(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.get(self.exists_blog_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BlogEditView.title)

    def test_new_by_admin_post(self):
        self.client.login(username=self.admin_email, password=self.admin_password)
        response = self.client.post(
            self.exists_blog_edit_url,
            data=dict(
                title=self.exists_blog.title,
                body='bla-bla',
                status=Blog.STATUSES.draft,
                tags='tag1, tag2',
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('blog_detail', kwargs=dict(slug=self.exists_blog.slug)), response.url)
        blog = Blog.objects.get(slug=self.exists_blog.slug)
        self.assertEqual(blog.body, 'bla-bla')
        self.assertEqual(blog.status, Blog.STATUSES.draft)

