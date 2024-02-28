from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Profile, ChatRoom
from ..serializers import ProfileSerializer, ChatRoomSerializer


# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']):
#         return Response("missing user", status=status.HTTP_404_NOT_FOUND)
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = ProfileSerializer(user)
#     return Response({'token': token.key, 'user': serializer.data})


@api_view(['GET', 'PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request, pk):
    try:
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        print('arquivos ', request.FILES)
        if request.method == 'PATCH':
            if 'photo' in request.FILES:
                profile.profile_picture = request.FILES['photo']

            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                profile.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)


@api_view(['POST'])
def create_chatroom(request):
    # Obter IDs dos perfis dos dados enviados na solicitação
    profile1_id = request.data.get('profile1_id')
    profile2_id = request.data.get('profile2_id')

    # Verificar se os IDs foram fornecidos
    if not profile1_id or not profile2_id:
        return Response({"error": "IDs dos perfis não fornecidos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Obter perfis do banco de dados
        profile1 = Profile.objects.get(id=profile1_id)
        profile2 = Profile.objects.get(id=profile2_id)
    except Profile.DoesNotExist:
        return Response({"error": "Perfil não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Verificar se já existe um chatroom entre os dois perfis
    existing_chatroom = ChatRoom.objects.filter(
        members=profile1
    ).filter(
        members=profile2
    )

    if existing_chatroom.exists():
        # Se um chatroom já existir, retornar um erro
        return Response({"error": "Já existe um chatroom entre esses perfis"})

    # Criar um novo chatroom
    chatroom = ChatRoom.objects.create()

    # Adicionar perfis como membros do chatroom
    chatroom.members.add(profile1)
    chatroom.members.add(profile2)

    # Serializar o chatroom criado
    serializer = ChatRoomSerializer(chatroom)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
