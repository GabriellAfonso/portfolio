import requests
from rest_framework.views import APIView
from .models import Profile
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# verificar que os usuarios existem
# verificar se o sender tem saldo
# consultar altorizaçao
# verificar se quem ta mandando é conta normal


class TransactionRest(APIView):

    def post(self, request):
        value = request.data.get('value')
        sender = request.data.get('sender')
        receiver = request.data.get('receiver')
        data = {
            'value': value,
            'sender': sender,
            'receiver': receiver,
        }
        if not self.profiles_exists(sender, receiver):
            return Response({"error": "perfis não encontrados"}, status=status.HTTP_400_BAD_REQUEST)
        if not self.sender_balance_validate(sender, value):
            return Response({"error": "Saldo insuficiente!"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.get_authorization():
            return Response({'error': 'Transação não autorizada'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Transação autorizada e processada com sucesso'}, status=status.HTTP_200_OK)

    def profiles_exists(self, profile1, profile2):
        return (
            Profile.objects.filter(user_id=profile1).exists() and
            Profile.objects.filter(user_id=profile2).exists()
        )

    def sender_balance_validate(self, sender, value):
        sender_data = get_object_or_404(Profile, user_id=sender)
        if sender_data.balance < value:
            return False

        return True

    def get_authorization(self):
        external_service_url = 'https://util.devi.tools/api/v2/authorize'
        try:
            response = requests.get(external_service_url)
            response_data = response.json()
            if response.status_code == 200 and response_data.get('data', {}).get('authorization'):
                return True
            else:
                return False

        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
