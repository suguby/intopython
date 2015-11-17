from django.db import models


class BlogRecord(models.Model):
    title = models.CharField(max_length=64, null=True)
    message = models.TextField(null=True)

    class Meta:
        db_table = 'blog_records'

    def __str__(self):
        return 'BlogRecord({}, {})'.format(self.id, self.title)
