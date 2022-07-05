from rest_framework import serializers
from user.models import User, UserProfile
from django.contrib.auth.hashers import make_password

class UserProfileSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSeiralizer(read_only=True)

    def create(self, validated_data):
        validated_data['is_active'] = True
        password = validated_data.pop('password')
        new_user = User(**validated_data)
        new_user.set_password(password)
        new_user.save()

        return validated_data

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'error_messages': {
                    'required': '이메일을 입력해주세요.',
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                },
                'required': False
            },
            'birthday': {
                'error_messages': {
                    'required': '생년월일을 입력해주세요.',
                },
                'required': False
            },
        }
