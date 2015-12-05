from django.db import models

class BlogRecord(models.Model):
    title = models.CharField(max_length=64)
    message = models.TextField()

    def __str__(self):
        return 'BlogRecord: {}'.format(self.title)