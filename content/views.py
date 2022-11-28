from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed, Like, Bookmark, Reply
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
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            # 댓글들
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))
            # 피드
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=feed.like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  reply_list=reply_list
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

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        is_like = request.data.get('is_like', True)

        if is_like == "true" or is_like == 'True':
            is_like = True
        else:
            is_like = False

        email = request.session.get('email', None)

        Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)