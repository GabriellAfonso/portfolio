import requests
from rest_framework.views import APIView
from .models import PicPayAccount
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .validators import TransactionValidator
from .exceptions import TransactionExceptions
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

# verificar que os usuarios existem
# verificar se o sender tem saldo
# consultar altorizaçao
# verificar se quem ta mandando é conta normal


class TransactionRest(APIView):

    @method_decorator(csrf_protect)
    def post(self, request):
        value = self.process_value(request.data.get('value'))
        print('value', value)
        sender = self.get_sender(request.user.id)
        print('eu', sender)
        receiver = self.get_receiver(request.data.get('document'))
        print('quem', receiver)
        data = {
            'value': value,
            'sender': sender,
            'receiver': receiver,
        }
        transaction = TransactionValidator()
        try:
            transaction.validate(data)
        except TransactionExceptions as e:

            return Response({'validation_error': e.message}, status=e.status_code)
        except Exception as e:
            print(str(e))
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'Success': 'Transação autorizada e processada com sucesso'}, status=status.HTTP_200_OK)

    def process_value(self, value):
        v1 = value.replace('.', '')
        v2 = v1.replace(',', '.')
        return float(v2)

    def get_sender(self, id):
        sender = PicPayAccount.objects.get(user_id=id)
        return sender.id

    def get_receiver(self, doc):
        receiver = PicPayAccount.objects.get(document=doc)
        return receiver.id
