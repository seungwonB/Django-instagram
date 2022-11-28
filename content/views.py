from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed
from rest_framework.response import Response
import os
from Jinstagram.settings import MEDIA_ROOT
from uuid import uuid4
from user.models import User


class Main(APIView):
    def get(self, request):
        feed_object_list = Feed.objects.all().order_by('-id')  # 피드에 있는 모든 데이터를 가져옴(쿼리셋) = select * from content_feed, 최신 글을 위한 역순 출력
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            feed_list.append(dict(image=feed.image,
                                  content=feed.content,
                                  like_count=feed.like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname
                                  ))

        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if email is None:
            return render(request, 'user/login.html')

        return render(request, 'jinstagram/main.html', context=dict(feed_list=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        # 일단 파일 불러오기
        file = request.FILES['file']
        # 특수문자, 한글 등이 오면 오류가 나서 랜덤으로 id값(영어+숫자)
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        # 파일 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        email = request.session.get('email', None)

        # 피드에 나타내기
        Feed.objects.create(content=content, image=image, email=email, like_count=0)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if email is None:
            return render(request, 'user/login.html')

        return render(request, 'content/profile.html', context=dict(user=user))
