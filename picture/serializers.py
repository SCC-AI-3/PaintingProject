from rest_framework import serializers
from .models import Picture, Category, Comment
from datetime import datetime
from user.serializers import UserSerializer
from django.utils import dateformat, timezone


class CategorySeiralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_created_at(self, obj):
        return dateformat.format(obj.created_at, 'y.m.d H시 i분')

    class Meta:
        model = Comment
        fields = "__all__"


class PictureSeiralizer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField(read_only=True)

    def get_image_path(self, obj):
        return 'http://127.0.0.1:8000'+obj.image.url
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        return obj.user.username

    # commentfile = commentSeiralizer()
    # Categoryfile = CategorySeiralizer()
    def create(self, validated_data):
        # User object 생성
        picture = Picture(**validated_data)
        print(picture)
        picture.save()
        return validated_data

    def update(self, instance, validated_data):
        today = datetime.today().strftime("%Y-%m-%d")
        for key, value in validated_data.items():
            if key == "Contents":
                value += f' {today}에 수정된 상품입니다.'
                continue
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = Picture
        fields = ["image", "description", "username", "user", "image_path"]
