from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from src.articles.models import Article
from src.common.models import AbstractModel


class ScreencastSection(AbstractModel):
    STATUSES = Article.STATUSES

    title = models.CharField(verbose_name='Заголовок', max_length=128, default='')
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True, unique=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    status = models.CharField(verbose_name='Статус', max_length=16, choices=STATUSES, default=STATUSES.draft)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'screencast_sections'

    _str_template = ' "{title}" / {modified_at} / {status}'

    def save(self, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super().save(**kwargs)


class Screencast(Article):
    section = models.ForeignKey(ScreencastSection, verbose_name='Раздел', related_name='screencasts')
    video = models.TextField(verbose_name='Видео', default='')

    class Meta:
        db_table = 'screencasts'

    def save(self, **kwargs):
        self.type = Article.TYPES.screencast
        super().save(**kwargs)

    def iframe(self):
        iframe = self.video.replace('<iframe', '<iframe class="lesson-video" ')
        return iframe


class ScreencastEdit(Screencast):

    class Meta:
        pass
