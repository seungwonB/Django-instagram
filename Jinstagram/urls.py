from django.contrib import admin
from django.urls import path, include
from .views import Sub
from content.views import Main
from content.views import UploadFeed
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static


urlpatterns = [
    path('', Main.as_view()),
    # 다른 앱에 있는 url
    path('content/',include('content.urls')),
    path('user/', include('user.urls'))
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)