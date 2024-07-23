from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='picpay_profile')
    complete_name = models.CharField(max_length=50)
    document = models.CharField(max_length=100)
    document_type = models.CharField(max_length=4, choices=[
        ('cpf', 'CPF'), ('cnpj', 'CNPJ')])
    sex = models.CharField(max_length=1, choices=[
                           ('M', 'Masculino'), ('F', 'Feminino')])
    account_type = models.CharField(max_length=10, choices=[(
        'personal', 'Personal'), ('merchant', 'Merchant')])
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id:{self.id} {self.user.email}'


class Transaction(models.Model):
    value = ''
    sender = ''
    receiver = ''
    created_at = models.DateTimeField(auto_now_add=True)
