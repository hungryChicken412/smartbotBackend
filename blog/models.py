from django.db import models
from datetime import datetime

from tinymce.widgets import TinyMCE


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    background = models.FileField(default=None, upload_to="blog")
    brief = models.TextField(max_length=150, default='')
    published = models.DateTimeField(
        'date published', default=datetime.now)

    def __str__(self):
        return self.title+str(self.published)
