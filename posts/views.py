from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from posts.models import *
from django.utils import timezone
from datetime import timedelta

from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import KeyHeaderPermission, IsPostAuthor
import os

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-12th!"
        })
    
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def get_recent_posts(request):
    if request.method == "GET":
        one_week_ago = timezone.now() - timedelta(weeks=1)
        recent_posts = Post.objects.filter(created_at__gte=one_week_ago).order_by('-created_at')
        recent_posts_json = []
    
        for post in recent_posts:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "writer": post.writer,
                "created_at": post.created_at,
                "category": post.category
            }
            recent_posts_json.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '최근 일주일 내 작성된 게시글 목록 조회 성공',
            'data': recent_posts_json
        })

class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [KeyHeaderPermission]
        else: 
            self.permission_classes = [KeyHeaderPermission, IsAuthenticated]
        return super(PostListAPIView, self).get_permissions()
    
    # @Override
    def create(self, request, *args, **kwargs):
        thumbnail = request.data.get('thumbnail')
        if thumbnail: 
            ext = os.path.splitext(thumbnail.name)[1]
            if ext.lower() == ".png":
                return Response(".png extensions not allowed", status=status.HTTP_400_BAD_REQUEST)
        return super(PostListAPIView, self).create(request, *args, **kwargs)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [KeyHeaderPermission, IsPostAuthor, IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'pid'
    
class CommentList(APIView):
    permission_classes = [KeyHeaderPermission, IsAuthenticated]
    def get(self, request, pid):
        comments = Comment.objects.filter(post_id=pid)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, pid):    
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = [KeyHeaderPermission, IsAuthenticated]
    def get(self, request, cid): #'request' formal param 적어주자, 안 적으면 에러남 
        comment = get_object_or_404(Comment, id=cid)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, cid):
        comment = get_object_or_404(Comment, id=cid)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cid):
        comment = get_object_or_404(Comment, id=cid)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
