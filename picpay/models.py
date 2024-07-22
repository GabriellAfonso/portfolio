from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='picpay_profile')
    document = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=[
                           ('M', 'Masculino'), ('F', 'Feminino')])
    type = models.CharField(max_length=10, choices=[(
        'personal', 'Personal'), ('merchant', 'Merchant')])
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.email
