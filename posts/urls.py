from django.urls import path
from posts.views import *

urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('<int:pid>/', PostDetailAPIView.as_view()),
    path('<int:pid>/comments/', CommentList.as_view()),
    path('comments/<int:cid>/', CommentDetail.as_view()),
]