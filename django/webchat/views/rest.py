from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Profile, ChatRoom, Message
from ..serializers import ProfileSerializer, ChatRoomSerializer, MessageSerializer


class UserProfile(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            profile = get_object_or_404(Profile, pk=pk)
            if 'photo' in request.FILES:
                profile.profile_picture = request.FILES['photo']

            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateChatroom(APIView):

    def post(self, request):
        profile1_id = request.data.get('profile1_id')
        profile2_id = request.data.get('profile2_id')

        try:
            profile1 = Profile.objects.get(id=profile1_id)
            profile2 = Profile.objects.get(id=profile2_id)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found!"}, status=status.HTTP_404_NOT_FOUND)

        if self.__chatroom_exists(profile1, profile2):
            return Response({"error": "There is already a chatroom between these profiles"})

        return self.__create_new_chatroom(profile1, profile2)

    def __chatroom_exists(self, profile1, profile2):
        existing_chatroom = ChatRoom.objects.filter(
            members=profile1
        ).filter(
            members=profile2
        )

        return existing_chatroom.exists()

    def __create_new_chatroom(self, profile1, profile2):
        chatroom = ChatRoom.objects.create()

        chatroom.members.add(profile1)
        chatroom.members.add(profile2)

        serializer = ChatRoomSerializer(chatroom)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_messages(request, chatroom_id):
    chatroom = ChatRoom.objects.get(pk=chatroom_id)

    # Verifica se o usuário atual está entre os membros da sala de chat
    if request.user.profile not in chatroom.members.all():
        return Response({"error": "Você não tem permissão para visualizar mensagens nesta sala de chat."}, status=status.HTTP_403_FORBIDDEN)

    chatroom_serializer = ChatRoomSerializer(chatroom)
    messages = Message.objects.filter(room=chatroom)
    message_serializer = MessageSerializer(messages, many=True)

    response_data = {
        'chatroom': chatroom_serializer.data,
        'messages': message_serializer.data
    }

    return Response(response_data)


@api_view(['GET', 'POST'])
def send_message(request, chatroom_id):
    chatroom = ChatRoom.objects.get(pk=chatroom_id)

    # Verifica se o usuário atual está entre os membros da sala de chat
    if request.user.profile not in chatroom.members.all():
        return Response({"error": "Você não tem permissão para enviar mensagens para esta sala de chat."}, status=status.HTTP_403_FORBIDDEN)

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(room=chatroom, sender=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
