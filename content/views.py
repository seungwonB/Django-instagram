from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id') # 피드에 있는 모든 데이터를 가져옴(쿼리셋) = select * from content_feed, 최신 글을 위한 역순 출력
        
        return render(request, 'jinstagram/main.html', context = dict(feed_list=feed_list))


