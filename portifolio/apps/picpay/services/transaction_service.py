from apps.picpay.models import Transaction
from apps.picpay.exceptions import AuthorizationDenied
import requests
from django.db import transaction as django_transaction

from apps.picpay.validators.transaction_validator import TransactionValidator


class TransactionService():

    def process_transaction(self, data):
        validator = TransactionValidator()
        validator.validate(data)
        sender = data['sender']
        receiver = data['receiver']
        transaction = self._perform_transfer(data['value'], sender, receiver)
        return transaction

    def _get_external_authorization(self):
        external_service_url = 'https://util.devi.tools/api/v2/authorize'

        response = requests.get(external_service_url)
        response_data = response.json()
        if response.status_code == 200 and response_data.get('data', {}).get('authorization'):
            return True
        raise AuthorizationDenied

    def _perform_transfer(self, value, sender, receiver):
        transaction_value = value
        with django_transaction.atomic():
            self._get_external_authorization()
            sender.pay(transaction_value)
            receiver.receive(transaction_value)

            transactionDB = Transaction(
                sender=sender,
                receiver=receiver,
                value=transaction_value,
            )

            sender.save()
            receiver.save()
            transactionDB.save()
            return transactionDB
