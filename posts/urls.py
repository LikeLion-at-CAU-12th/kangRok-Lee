from django.urls import path
from posts.views import *

urlpatterns = [
    path('', post_list, name = 'post_list'),
    path('<int:id>/comments', comment_list, name="comment_list"),
    path('page', index, name='my-page'),
    path('introduction', introduction, name="peer-intro"),
    path('<int:id>', post_detail, name = "게시글 조회"),
]