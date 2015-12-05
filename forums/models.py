from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    position = models.IntegerField(_('Position'), default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name


class Forum(models.Model):
    category = models.ForeignKey(Category, related_name='forums')
    name = models.CharField(_("Name"), max_length=255)
    position = models.IntegerField(_("Position"), default=0)
    description = models.TextField(_("Description"), blank=True)
    is_closed = models.BooleanField(_("Is closed"), default=False)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    @property
    def count_topics(self):
        return Topic.objects.filter(forum=self).count()

    @property
    def count_posts(self):
        return Post.objects.filter(topic__forum=self).count()

    @property
    def get_last_post(self):
        try:
            return Post.objects.filter(topic__forum=self).last()
        except Post.DoesNotExist:
            pass

    @permalink
    def get_absolute_url(self):
        return 'forum:forum_detail', [self.id]


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics')
    name = models.CharField(_("Name"), max_length=255)

    class Meta:
        ordering = ['-id']

    @permalink
    def get_absolute_url(self):
        return 'forum:topic_detail', [self.id]

    def __str__(self):
        return self.name

    @property
    def count_posts(self):
        return Post.objects.filter(topic=self).count()

    @property
    def get_last_post(self):
        try:
            return Post.objects.filter(topic=self).last()
        except Post.DoesNotExist:
            pass

    @property
    def get_author_topic(self):
        try:
            return Post.objects.filter(topic=self).first().user
        except Post.DoesNotExist:
            pass


class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='forum_posts')
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    body = models.TextField(_("Body"))

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body

    @property
    def get_absolute_url(self):
        topic_url = reverse('forum:topic_detail', args=[self.topic.pk])
        return '{}#post-{}'.format(topic_url, self.pk)
