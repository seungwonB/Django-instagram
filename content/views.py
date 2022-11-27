from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feed
from uuid import uuid4
import os
from Jinstagram.settings import MEDIA_ROOT

class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id') # 피드에 있는 모든 데이터를 가져옴(쿼리셋) = select * from content_feed, 최신 글을 위한 역순 출력
        
        return render(request, 'jinstagram/main.html', context = dict(feed_list=feed_list))

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

        file = request.data.get('file')
        image = request.data.get('image')
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        # 피드에 나타내기
        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        return Response(status=200)
