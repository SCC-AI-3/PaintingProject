from django.contrib import admin
from django.urls import path
from user import views
from user.views import CustomTokenObtainPairView, OnlyAuthenticatedUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # 기본 jwt access 토큰 발급 view
    TokenRefreshView,  # jwt refresh 토큰 발급 view
)

urlpatterns = [
    path('', views.UserView.as_view()),
    path('register/', views.UserView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_refresh'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/authonly/', OnlyAuthenticatedUserView.as_view)
    # path('login/', views.UserAPIView.as_view()),
    # path('logout/', views.UserAPIView.as_view()),
]
