from rest_framework import serializers
from .models import User,UserProfile


class UserProfileSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class UserSeiralizer(serializers.ModelSerializer):
    userprofile = UserProfileSeiralizer()
    class Meta:
        model = User
        fields = "__all__"