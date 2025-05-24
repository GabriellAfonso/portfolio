from apps.picpay.models import Transaction
from django.db.models import Q
from django.utils.timezone import now
from apps.picpay.utils import get_first_and_last_name


def get_last_transactions(account):
    last_transactions = (
        Transaction.objects
        .filter(Q(sender=account) | Q(receiver=account))
        .select_related('sender', 'receiver')
        .order_by('-created_at')[:3]
    )

    processed_transactions = []
    for transaction in last_transactions:

        if transaction.sender_id == account.id:
            action = "Enviou"
            counterpart = transaction.receiver.complete_name
        else:
            action = "Recebeu"
            counterpart = transaction.sender.complete_name

        time_elapsed = now() - transaction.created_at
        days_ago = time_elapsed.days
        if days_ago == 0:
            time_str = "Hoje"
        elif days_ago == 1:
            time_str = "Ontem"
        else:
            time_str = f"{days_ago} dias atrás"

        processed_transactions.append({
            'action': action,
            'time': time_str,
            'value': transaction.value,
            'counterpart': get_first_and_last_name(counterpart)
        })

    return processed_transactions
