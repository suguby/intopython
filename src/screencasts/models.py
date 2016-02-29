from django.db import models

from src.articles.models import Article
from src.common.models import AbstractModel
from src.common.utils import get_translit


class ScreencastSection(AbstractModel):
    title = models.CharField(verbose_name='Заголовок', max_length=128, default='')
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'screencast_sections'

    _str_template = ' "{title}" / {modified_at}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = get_translit(self.title)
        super(ScreencastSection, self).save(force_insert=force_insert, force_update=force_update,
                                            using=using, update_fields=update_fields)


class Screencast(Article):
    section = models.ForeignKey(ScreencastSection, verbose_name='Раздел', related_name='screencasts')
    video = models.TextField(verbose_name='Видео', default='')

    class Meta:
        db_table = 'screencasts'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.type = Article.TYPES.screencast
        super(Screencast, self).save(force_insert=force_insert, force_update=force_update,
                                     using=using, update_fields=update_fields)
