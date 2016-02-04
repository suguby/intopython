from django.db import models

from articles.models import Article, ArticleByTypeManager


class Blog(Article):
    tag = models.CharField(max_length=100, verbose_name='Таги', null=True, blank=True)

    class Meta:
        db_table = 'blogs'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.type = Article.TYPES.blog
        super(Blog, self).save(
            force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields)
