from distutils.command.upload import upload
from django.db import models

# Create your models here.


from django.db import models

class User(models.Model):
    username = models.CharField("사용자 계정", max_length=20, unique=True)
    email = models.EmailField("이메일 주소", max_length=100, unique=True)
    password = models.CharField("비밀번호", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(to=User, verbose_name="사용자", on_delete=models.CASCADE)
    introduction = models.TextField("소개")
    birthday = models.DateField("생일")
    image = models.ImageField(upload_to = '')