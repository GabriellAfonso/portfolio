from rest_framework.views import APIView
from .models import PicPayAccount
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from .exceptions import TransactionExceptions
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.picpay.services.transaction_service import TransactionService


class TransactionAPIView(APIView):
    """
    API REST para processar transações PicPay.
    """

    def get(self, request):
        serializer = TransactionSerializer()
        return Response(serializer.data)

    @method_decorator(csrf_protect)
    def post(self, request):
        try:
            value = self.process_value(request.data.get('value'))
            sender = self.get_sender(request.user.id)
            receiver = self.get_receiver(request.data.get('document'))

            data = {
                'value': value,
                'sender': sender,
                'receiver': receiver,
            }

            transaction = TransactionService()
            transaction_process = transaction.process_transaction(data)
            serializer = TransactionSerializer(transaction_process)
            return Response(
                {'success': 'Transação autorizada e processada com sucesso',
                 'transaction': serializer.data},
                status=status.HTTP_201_CREATED
            )

        except TransactionExceptions as e:
            return Response({'detail': e.message}, status=e.status_code)

        except PicPayAccount.DoesNotExist:
            return Response({'detail': 'Conta não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        # except Exception as e:
        #     return Response({'detail': 'Erro interno ao processar a transação.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_value(self, value):
        v1 = value.replace('.', '')
        v2 = v1.replace(',', '.')
        return float(v2)

    def get_sender(self, id):
        sender = PicPayAccount.objects.get(user_id=id)
        return sender

    def get_receiver(self, doc):
        receiver = PicPayAccount.objects.get(document=doc)
        return receiver
