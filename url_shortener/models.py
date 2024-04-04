from django.db import models


class URL(models.Model):
    long_url = models.URLField(unique=True)
    short_url = models.CharField(max_length=40, unique=True)
