from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('register/', views.UserView.as_view()),
    path('login/', views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
]