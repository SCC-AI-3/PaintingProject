from django.urls import path
from . import views
# from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.PictureView.as_view(), name='picture'),
    # path('<obj_id>/', views.PictureView.as_view()),
    path('mygallery/', views.mygalleryView.as_view()),
    path('usergallery/<int:user_id>', views.usergalleryView.as_view()),
    path('picture/<int:picture_id>', views.pictureView.as_view()),
    path('comment/<int:comment_id>', views.CommentView.as_view()),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
