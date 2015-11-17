from django.db import models
from model_utils import Choices


class ScreencastSection(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=128, default='')
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'screencast_sections'

    def __str__(self):
        return 'Раздел "{}" / {}'.format(self.title, self.modified_at)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = self.title
        super(ScreencastSection, self).save(force_insert=force_insert, force_update=force_update,
                                            using=using, update_fields=update_fields)


class Screencast(models.Model):
    STATUSES = Choices(('draft', 'Черновик'), ('publ', 'Опубликовано'), ('hided', 'Скрыто'), )

    section = models.ForeignKey(ScreencastSection, verbose_name='Раздел')
    title = models.CharField(verbose_name='Заголовок', max_length=128, default='')
    video = models.TextField(verbose_name='Видео', default='')
    summary = models.TextField(verbose_name='Конспект', null=True)
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    status = models.CharField(verbose_name='Статус', max_length=16, choices=STATUSES, default=STATUSES.draft)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'screencasts'

    def __str__(self):
        return 'Скринкаст "{}" / {}'.format(self.title, self.modified_at)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = self.title
        super(Screencast, self).save(force_insert=force_insert, force_update=force_update,
                                     using=using, update_fields=update_fields)
