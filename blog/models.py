from django.db import models

class BlogRecord(models.Model):
    title = models.CharField(max_length=64)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return 'BlogRecord: {}'.format(self.title)