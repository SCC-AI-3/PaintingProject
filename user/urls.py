from django.contrib import admin
from django.urls import path
from user import views
from user.views import CustomTokenObtainPairView, MyPageView, UserAdjustView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # 기본 jwt access 토큰 발급 view
    TokenRefreshView,  # jwt refresh 토큰 발급 view
)

urlpatterns = [
    path('', views.UserView.as_view()),
    path('register/', views.UserView.as_view()),  # 회원가입 url
    path('login/', CustomTokenObtainPairView.as_view()),  # 로그인 url
    path('put/', UserAdjustView.as_view()),  # 회원정보 수정 url
    path('delete/', UserAdjustView.as_view()),  # 회원탈퇴 url
    path('mypage/', MyPageView.as_view()),  # 마이페이지
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]