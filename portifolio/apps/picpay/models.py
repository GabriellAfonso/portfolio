from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class PicPayAccount(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,)
    complete_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    document = models.CharField(max_length=100, unique=True)
    document_type = models.CharField(max_length=4, choices=[
        ('cpf', 'CPF'), ('cnpj', 'CNPJ')])
    sex = models.CharField(max_length=1, choices=[
                           ('M', 'Masculino'), ('F', 'Feminino')])
    account_type = models.CharField(max_length=10, choices=[(
        'personal', 'Personal'), ('merchant', 'Merchant')])
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def pay(self, value):
        value = Decimal(value)  # Converte o valor para Decimal
        self.balance -= value
        self.save()

    def receive(self, value):
        value = Decimal(value)  # Converte o valor para Decimal
        self.balance += value
        self.save()

    def __str__(self):
        return f'id:{self.id} {self.user.email}'


class Transaction(models.Model):
    value = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False)
    sender = models.ForeignKey(
        PicPayAccount, related_name='sent_transactions', on_delete=models.CASCADE, editable=False)
    receiver = models.ForeignKey(
        PicPayAccount, related_name='received_transactions', on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
