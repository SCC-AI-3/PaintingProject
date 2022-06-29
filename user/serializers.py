from rest_framework import serializers
from .models import User,UserProfile


class UserSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
