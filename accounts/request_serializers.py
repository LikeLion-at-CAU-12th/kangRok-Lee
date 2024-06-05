from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User
from allauth.socialaccount.models import SocialAccount

class OAuthSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, data):
        email = data.get("email", None)
        
        user = User.get_user_or_none_by_email(email=email)

        #애초에 해당 이메일로 가입이 안되어있다면
        if user is None:
            raise serializers.ValidationError("user account not exists")

        try:
            social_user = SocialAccount.objects.get(user=user)  # 소셜로그인 계정 유무 확인
        except SocialAccount.DoesNotExist: #소셜로그인을 사용하지 않는 유저
            raise serializers.ValidationError("No social account associated with this user")

        if social_user.provider != 'google': #있긴한데 구글 로그인이 아닐때 (eg. 카카오, 깃헙 등등)
            raise serializers.ValidationError("only Google login is supported")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data