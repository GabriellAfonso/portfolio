import requests
from apps.picpay.models import PicPayAccount, Transaction
from django.db import transaction as django_transaction
from rolepermissions.checkers import has_permission
from apps.picpay.exceptions import (
    AccountDoesNotExist, SelfTransferError,
    InsufficientBalanceError,
    TransferPermissionDenied,
    ReceivePermissionDenied, )
from django.core.exceptions import ValidationError


class TransactionValidator():

    def validate(self, data):
        sender = data['sender']
        receiver = data['receiver']
        self.check_positive_value(data['value'])
        self.check_not_self_transfer(sender, receiver)
        self.check_balance_sufficient(sender, data['value'])
        self.check_permissions(sender, receiver)

    def check_positive_value(self, value):
        if value <= 0:
            raise ValidationError("O valor da transação deve ser positivo.")

    def check_not_self_transfer(self, sender, receiver):
        if sender.id == receiver.id:
            raise SelfTransferError

    def check_balance_sufficient(self, sender, value):
        if sender.balance < value:
            raise InsufficientBalanceError(sender)

    def check_permissions(self, sender, receiver):
        if not has_permission(sender.user, 'make_transfer'):
            raise TransferPermissionDenied
        elif not has_permission(receiver.user, 'receive_transfer'):
            raise ReceivePermissionDenied
