from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('page', index, name='my-page'),
    path('introduction', introduction, name="peer-intro")
]