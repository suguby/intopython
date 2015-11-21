from django.db import models


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    position = models.IntegerField(_('Position'), default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name