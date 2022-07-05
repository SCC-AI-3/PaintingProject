from django.urls import path
from . import views

urlpatterns = [
    path('', views.PictureView.as_view(),name='picture'),
    path('<obj_id>/', views.PictureView.as_view()),
]

