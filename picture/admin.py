from django.contrib import admin
from picture.models import Picture,Comment,Category
# Register your models here.
admin.site.register(Picture)
admin.site.register(Comment)
admin.site.register(Category)
