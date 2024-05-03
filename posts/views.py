from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from posts.models import *
from django.utils import timezone
from datetime import timedelta

# Create your views here.
import json

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-12th!"
        })
    
def index(request):
    return render(request, 'index.html')

def introduction(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data' : [
                {
                    "name" : "이강록",
                    "age" : 22,
                    "major" : "CSE"
                },
                {
                    "name" : "박채린",
                    "age" : 21,
                    "major" : "CSE"
                }
            ]
        })
    
@require_http_methods(["GET"])
def get_post_detail(request,id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "writer" : post.writer,
        "category" : post.category,
    }

    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'data' : post_detail_json
    })

@require_http_methods(["POST", "GET"])
def post_list(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))

        # new_post는 QuerySet!
        new_post = Post.objects.create(
            writer = body['writer'],
            title = body['title'],
            content = body['content'],
            category = body['category']
        )

        new_post_json = {
            # id 는 AutoField
            "id": new_post.id,
            "writer": new_post.writer,
            "title" : new_post.title,
            "content": new_post.content,
            "category": new_post.category
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json
        })
    
    if request.method == "GET":
        post_all = Post.objects.all()
        post_json_all = []

        for post in post_all:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "writer": post.writer,
                "category": post.category
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all
        })

@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    if request.method == "GET":
        post = get_object_or_404(Post, pk=id)

        post_json = {
            "id": post.id,
            "writer": post.writer,
            "title" : post.title,
            "content": post.content,
            "category": post.category,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 조회 성공',
            'data': post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))

        update_post = get_object_or_404(Post, pk=id)

        update_post.title = body['title']
        update_post.content = body['content']
        update_post.category = body['category']

        update_post.save()

        update_post_json = {
            "id": update_post.id,
            "writer": update_post.writer,
            "title": update_post.title,
            "content": update_post.content,
            "category": update_post.category
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=id)
        delete_post.delete()

        return JsonResponse({
            'status': 200,
            'message': '게시글 삭제 성공',
            'data': None
        })

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

@require_http_methods(["GET"])
def comment_list(request, id):
    if request.method == "GET":
        comment_all = Comment.objects.filter(post_id=id)
        comment_json_all = []

        for comment in comment_all:
            comment_json = {
                "id": comment.id,
                "writer": comment.writer,
                "content": comment.content
            }
            comment_json_all.append(comment_json)

        return JsonResponse({
            'status': 200,
            'message': 'fetched all comments',
            'data': comment_json_all
        })
    

from .serializers import PostSerializer, CommentSerializer

# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    def get(self, request, pid):
        post = get_object_or_404(Post, id=pid)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pid):
        post = get_object_or_404(Post, id=pid)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pid):
        post = get_object_or_404(Post, id=pid)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentList(APIView):
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
    
