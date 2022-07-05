from user.jwt_claim_serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


# 삭제 해요?
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
#


from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from user.serializers import UserSerializer


# Create your views here.

class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "get method"})

    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            # return redirect('login')
            return Response({"message": "회원가입 성공"})

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAdjustView(APIView):  # 회원정보 수정 및 삭제
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if user:
            user.delete()
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # serializer에 queryset을 인자로 줄 경우 many=True 옵션을 사용해야 한다.
        serialized_user_data = UserSerializer(user).data
        return Response(serialized_user_data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MyPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # token에서 인증된 user만 가져온다.
        user = request.user
        print(user)
        if not user:
            return Response({"error": "로그인을 해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        user_data = UserSerializer(user).data
        print(user_data)
        return Response({'user_data': user_data}, status=status.HTTP_200_OK)