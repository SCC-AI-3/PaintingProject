from user.jwt_claim_serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
#
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from user.serializers import UserSerializer


# Create your views here.
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보: {user}")
        if not user:
            return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Accepted"})


class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    # 마이페이지
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

    # 회원 정보 수정
    def put(self, request):
        return Response({"message": "put method!!"})

    # 회원 탈퇴
    def delete(self, request):
        return Response({"message": "delete method!!"})


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # serializer에 queryset을 인자로 줄 경우 many=True 옵션을 사용해야 한다.
        serialized_user_data = UserSerializer(user).data
        return Response(serialized_user_data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# class UserAPIView(APIView):
#     # 로그인
#     def post(self, request):
#         username = request.data.get('username', '')
#         password = request.data.get('password', '')

#         user = authenticate(request, username=username, password=password)
#         print(password)
#         if not user:
#             return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

#         login(request, user)
#         return Response({"message": "login success!!"})
#     # 로그아웃

#     def delete(self, request):
#         logout(request)
#         return Response({"message": "logout success!!"})
