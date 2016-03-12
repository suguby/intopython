from django.db import models
from django.db.models import Manager
from model_utils import Choices
from taggit.managers import TaggableManager

from src.common.models import AbstractModel
from src.common.utils import get_translit


class Article(AbstractModel):
    STATUSES = Choices(('draft', 'Черновик'), ('publ', 'Опубликовано'), ('hided', 'Скрыто'), )
    TYPES = Choices(('blog', 'Блог'), ('screencast', 'Скринкаст'))

    title = models.CharField(verbose_name='Заголовок', max_length=128, default='')
    summary = models.TextField(verbose_name='Конспект', null=True, blank=True)
    body = models.TextField(verbose_name='Содержание статьи', null=True, blank=True)

    slug = models.CharField(verbose_name='Слаг', max_length=128, db_index=True, blank=True)
    type = models.CharField(verbose_name='Тип', max_length=16, choices=TYPES, default=TYPES.screencast)
    status = models.CharField(verbose_name='Статус', max_length=16, choices=STATUSES, default=STATUSES.draft)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'articles'

    _str_template = ' "{title}" / {modified_at} / {status}'

    tags = TaggableManager()
    # TODO сделать slugify для русских тэгов http://django-taggit.readthedocs.org/en/latest/custom_tagging.html#TagBase

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = get_translit(self.title)
        super(Article, self).save(force_insert=force_insert, force_update=force_update,
                                  using=using, update_fields=update_fields)

    @property
    def tags_as_list(self):
        return self.tags.all()


class ArticleByTypeManager(Manager):

    def __init__(self, type=None):
        super(ArticleByTypeManager, self).__init__()
        self.type = type

    def get_query_set(self):
        return super(ArticleByTypeManager, self).get_query_set().filter(type=self.type)
