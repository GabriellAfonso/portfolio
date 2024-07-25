import requests
from .models import Account, Transaction
from django.db import transaction as django_transaction
from rolepermissions.checkers import has_permission
from .exceptions import (
    AccountDoesNotExist, SelfTransferError,
    InsufficientBalanceError,
    AuthorizationDenied, TransferPermissionDenied,
    ReceivePermissionDenied, )


class TransactionValidator():

    def __init__(self) -> None:
        pass

    def validate(self, data):
        self.sender = self.account_exists(data['sender'])
        self.receiver = self.account_exists(data['receiver'])
        self.check_same_account(self.sender, self.receiver)
        self.is_balance_sufficient(self.sender, data['value'])
        self.check_permissions()
        self.process_transaction(data['value'])

    def account_exists(self, account):
        if Account.objects.filter(id=account).exists():
            return Account.objects.get(id=account)
        raise AccountDoesNotExist(account)

    def check_same_account(self, sender, receiver):
        if sender.id == receiver.id:
            raise SelfTransferError

    def is_balance_sufficient(self, sender, value):
        if sender.balance < value:
            raise InsufficientBalanceError(sender)
        return True

    def check_permissions(self):
        if not has_permission(self.sender.user, 'make_transfer'):
            raise TransferPermissionDenied
        elif not has_permission(self.receiver.user, 'receive_transfer'):
            raise ReceivePermissionDenied
        return True

    def get_external_authorization(self):
        external_service_url = 'https://util.devi.tools/api/v2/authorize'

        response = requests.get(external_service_url)
        response_data = response.json()
        if response.status_code == 200 and response_data.get('data', {}).get('authorization'):
            return True
        raise AuthorizationDenied

    def process_transaction(self, value):
        transaction_value = value
        with django_transaction.atomic():
            self.sender.pay(transaction_value)
            self.receiver.receive(transaction_value)

            transactionDB = Transaction(
                sender=self.sender,
                receiver=self.receiver,
                value=transaction_value,
            )

            self.sender.save()
            self.receiver.save()
            transactionDB.save()
            self.get_external_authorization()
