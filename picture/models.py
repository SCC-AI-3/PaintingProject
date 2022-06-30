from django.db import models
from user.models import User
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50)    


class Picture(models.Model):
    user = models.ForeignKey(to=User, verbose_name="사용자", on_delete=models.CASCADE)
    description = models.TextField("소개")
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now_add=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to = 'picture')


class Comment(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    picture = models.ForeignKey(to=Picture,on_delete=models.CASCADE)    
    comment = models.TextField("댓글")
    created_at = models.DateTimeField("작성일", auto_now_add=True)

