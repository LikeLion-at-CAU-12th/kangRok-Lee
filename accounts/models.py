from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
    # 모델 내부 함수 구현
    @staticmethod
    def get_user_or_none_by_username(username):
        try:
            return User.objects.get(username=username)
        except Exception:
            return None
        
    @staticmethod
    def get_user_or_none_by_email(email):
        try:
            return User.objects.get(email=email)
        except Exception:
            return None
        
    # 근데 이러면 User.objects.filter(username)하고 뭐가 다른가??