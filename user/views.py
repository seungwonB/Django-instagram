from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User

class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # 회원가입
        email = request.data.get("email", None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.jpg")

        return Response(status=200)
class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # 로그인
        pass
