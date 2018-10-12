from django.db import models
from django.contrib.postgres.fields import JSONField


class Movie(models.Model):
    # the longest movie title I found was almost 200 chars long
    title = models.CharField(max_length=255)
    # I love 3NF but considering that OMDB API is undocumented it's the
    # fastest way to meet the requirements
    details = JSONField()
    # slugified title to quickly check movie existence
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)

    def __str__(self):
        return self.title
