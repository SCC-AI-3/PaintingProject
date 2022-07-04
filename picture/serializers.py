from rest_framework import serializers
from .models import Picture, Category, Comment
from datetime import datetime

class CategorySeiralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class commentSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PictureSeiralizer(serializers.ModelSerializer):
    # commentfile = commentSeiralizer()
    # Categoryfile = CategorySeiralizer()
    def create(self, validated_data):
        # User object 생성
        today = datetime.today().strftime("%Y-%m-%d")

        validated_data["description"] += f'{today}에 등록된 상품입니다.'
        picture = Picture(**validated_data)
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
        fields = ["image", "description","user","title"]
