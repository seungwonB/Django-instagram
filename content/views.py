from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feed
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id') # 피드에 있는 모든 데이터를 가져옴(쿼리셋) = select * from content_feed, 최신 글을 위한 역순 출력
        
        return render(request, 'jinstagram/main.html', context = dict(feed_list=feed_list))

class UploadFeed(APIView):
    def post(self, request):
        file = request.data.get('file')
        image = request.data.get('image')
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        return Response(status=200)
