from django.db import models
from model_utils import Choices


class ScreencastSection(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=128, default='')

    class Meta:
        db_table = "sc_sections"


class Screencast(models.Model):
    STATUSES = Choices(('draft', 'Черновик'), ('publ', 'Опубликовано'), ('hided', 'Скрыто'), )

    section = models.ForeignKey(ScreencastSection, verbose_name='Раздел')
    title = models.CharField(verbose_name='Заголовок', max_length=128, default='')
    video = models.TextField(verbose_name='Видео', default='')
    summary = models.TextField(verbose_name='Конспект', null=True)
    status = models.CharField(verbose_name='Статус', max_length=16, choices=STATUSES, default=STATUSES.draft)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True)
