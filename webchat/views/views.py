from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from webchat.forms import RegisterForm
from django.contrib import auth, messages
from django.contrib.auth import logout
from ..models import Profile, ChatRoom
from django.db.models.functions import Lower
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views import View
from django.utils.decorators import method_decorator


class Webchat(View):

    @method_decorator(login_required(login_url='webchat:login'))
    def get(self, request):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        user_chatrooms = self.__get_user_chatrooms_info(user_profile)
        profiles = self.__get_all_profiles()

        context = {
            'user_profile': user_profile,
            'user_chatrooms': user_chatrooms,
            'profiles': profiles,
        }

        return render(
            request,
            'webchat/webchat.html',
            context,
        )

    def __get_all_profiles(self):
        profiles = Profile.objects.all().annotate(
            lower_username=Lower('username')).order_by('lower_username')
        return profiles

    def __get_user_chatrooms_info(self, user):
        user_chatrooms = ChatRoom.objects.filter(members=user)

        chatrooms_member_info = []

        for chatroom in user_chatrooms:
            member = self.__get_member_except_user(chatroom, user)

            member_info = {
                'id': member.id,
                'profile_picture': member.profile_picture.url,
                'username': member.username,
            }

            chatrooms_member_info.append({
                'chatroom_id': chatroom.id,
                'member': member_info,
            })

        return chatrooms_member_info

    def __get_member_except_user(self, chatroom, user_profile):
        member = chatroom.members.exclude(user=user_profile.user).first()
        return member


class Login(View):

    def get(self, request):
        form = AuthenticationForm(request)
        context = {'form': form}

        return render(
            request,
            'webchat/login.html',
            context,
        )

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('webchat:chat')

        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('webchat:login')


def singup(request):

    form = RegisterForm()
    created_account = False

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            created_account = True
            context = {'created_account': created_account, }

            return render(
                request,
                'webchat/singup.html',
                context,
            )

        else:
            pass

    context = {
        'form': form,
        'created_account': created_account,
    }

    return render(
        request,
        'webchat/singup.html',
        context,
    )


@login_required(login_url='webchat:login')
def get_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    data = {'token': str(token)}

    return JsonResponse(data)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('webchat:login')
