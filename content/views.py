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
        feed_list = Feed.objects.all().order_by('-id') # 피드에 있는 모든 데이터를 가져옴(쿼리셋) = select * from content_feed, 최신 글을 위한 역순 출력

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

        content = request.data.get('content')
        image = uuid_name
        profile_image = request.data.get('profile_image')
        user_id = request.data.get('user_id')

        # 피드에 나타내기
        Feed.objects.create(content=content, image=image, profile_image=profile_image, user_id=user_id, like_count=0)

        return Response(status=200)
