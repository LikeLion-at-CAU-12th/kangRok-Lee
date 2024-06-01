# accounts/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import RegisterView

urlpatterns = [
    # 회원가입/로그인/로그아웃
    path("join/", RegisterView.as_view()),
    path("login/", AuthView.as_view()),
    path('logout/', LogoutView.as_view()),
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
]