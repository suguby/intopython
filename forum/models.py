from django.db import models


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
