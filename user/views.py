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
from picture.serializers import CommentSerializer
from picture.models import Picture, Comment


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
            return Response({"error": "로그인을 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user_data = UserSerializer(user).data
        print(user_data)
        return Response({'user_data': user_data}, status=status.HTTP_200_OK)


class CommentView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # # JWT 인증방식 클래스 지정하기
    # authentication_classes = [JWTAuthentication]

    # def post(self, request, id):
    # picture = Picture.objects.filter(id=id)
    def get(self, request):

        picture = Picture.objects.filter(id=5)  # 이거 게시글 아이디임
        comments = Comment.objects.filter(picture__in=picture)
        serialized_data = CommentSerializer(comments, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request):
        # user = request.user
        # request.data["user"] = user.id
        request.data["user"] = 2
        # request.data["picture"] = id
        request.data["picture"] = 2
        comment_serializer = CommentSerializer(
            data=request.data, context={"request": request})
        if comment_serializer.is_valid():
            comment_serializer.save()

            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = request.user
        comment = Comment.objects.get(id=id)
        if comment.user_id == user.id:
            comment.delete()
            return Response({"msg": "댓글 삭제"}, status=status.HTTP_200_OK)

        return Response({"msg": "권한 없음"}, status=status.HTTP_400_BAD_REQUEST)
