from django.db import models
from django.contrib.auth.models import User


class URL(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='urls')
    long_url = models.URLField(unique=False)
    short_url = models.CharField(max_length=40, unique=True)
