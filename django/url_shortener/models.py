from django.db import models
from django.contrib.auth.models import User


class URL(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='urls')
    long_url = models.URLField(unique=False)
    short_url = models.CharField(max_length=40, unique=True)

    MAX_URLS_PER_USER = 10  # Limite de URLs por usuário

    def save(self, *args, **kwargs):
        # Verifica se o usuário já tem 10 URLs
        if self.owner.urls.count() >= self.MAX_URLS_PER_USER:
            # Apaga a URL mais antiga
            oldest_url = self.owner.urls.order_by('id').first()
            oldest_url.delete()

        # Salva a nova URL
        super().save(*args, **kwargs)
