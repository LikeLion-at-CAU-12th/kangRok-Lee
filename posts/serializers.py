from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

    class Meta:
		# 어떤 모델을 시리얼라이즈할 건지
        model = Post
            # 모델에서 어떤 필드를 가져올지
            # 전부 가져오고 싶을 때
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"