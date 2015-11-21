from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255)
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


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics')
    name = models.CharField(_("Name"), max_length=255)
    last_post = models.ForeignKey(Post, verbose_name=_("Last post"),
                                  related_name='forum_last_post', blank=True, null=True)

    class Meta:
        ordering = ['-last_post__created']


