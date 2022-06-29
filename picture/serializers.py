from rest_framework import serializers
from .models import Picture, Category, comment


class CategorySeiralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class commentSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = "__all__"

class PictureSeiralizer(serializers.ModelSerializer):
    commentfile = commentSeiralizer()
    Categoryfile = CategorySeiralizer()
    class Meta:
        model = Picture
        fields = "__all__"
