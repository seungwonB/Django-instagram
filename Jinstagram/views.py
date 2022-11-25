from django.shortcuts import render
from rest_framework.views import APIView

class Sub(APIView):
    def get(self, request):
        print("get으로호출")
        return render(request, 'jinstagram/main.html')

    def post(self, request):
        return render(request, 'jinstagram/main.html')

