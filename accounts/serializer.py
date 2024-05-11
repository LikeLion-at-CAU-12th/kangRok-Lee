# accounts/serializers.py
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        #위에 적었는데 아래에 안 적으면 에러
        fields = ['password', 'username', 'email']

    def save(self, request):
        user = User.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )

        #encrypt pw
        user.set_password(self._validated_data['password'])
        user.save()

        return user
    
    def validate(self, data):
        email = data.get('email', None)
        # email에 KeyError오는걸 방지 위해서 data["email"]이렇게 가져오지 않는다.

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        
        return data
    
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        user = User.get_user_or_none_by_username(username=username)

        if user is None:
            raise serializers.ValidationError("user account not exist")
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError("wrong password")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data