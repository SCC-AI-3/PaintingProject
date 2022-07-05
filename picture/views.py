from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import PictureSeiralizer, CommentSerializer
from .models import Picture, Comment
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers import UserSerializer
from user.models import User


class PictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        picture = Picture.objects.order_by('-created_at')
        Picture_data = PictureSeiralizer(picture, many=True).data
        return Response({'Picture_data': Picture_data}, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        request.data['user'] = request.user.id
        Picture_serializer = PictureSeiralizer(data=request.data)
        if Picture_serializer.is_valid():
            # validator를 통과했을 경우 데이터 저장
            Picture_serializer.save()

            return Response({"message": "정상"}, status=status.HTTP_200_OK)

        return Response(Picture_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        picture = Picture.objects.get(id=obj_id)

        # 기본적인 사용 방법은 validator, creater와 다르지 않다.
        # update를 해줄 경우 obj, data(수정할 dict)를 입력한다.
        # partial=True로 설정해 주면 일부 필드만 입력해도 에러가 발생하지 않는다.
        Picture_serializer = PictureSeiralizer(
            picture, data=request.data, partial=True)
        if Picture_serializer.is_valid():
            # validator를 통과했을 경우 데이터 저장
            Picture_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        return Response(Picture_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class mygalleryView(APIView):
    def get(self, request):
        user = request.user
        bloger = User.objects.get(username=user)
        posts = Picture.objects.filter(user=user)
        pic_data = PictureSeiralizer(posts, many=True).data
        bloger_data = UserSerializer(bloger).data
        return Response({"posts": pic_data, "bloger": bloger_data}, status=status.HTTP_200_OK)


class usergalleryView(APIView):
    def get(self, request, user_id):
        bloger_id = User.objects.get(id=user_id)
        posts = Picture.objects.filter(user=user_id)
        pic_data = PictureSeiralizer(posts, many=True).data
        bloger_data = UserSerializer(bloger_id).data
        return Response({"posts": pic_data, "bloger": bloger_data}, status=status.HTTP_200_OK)


class pictureView(APIView):
    def get(self, request, picture_id):
        pic_id = Picture.objects.filter(id=picture_id)
        pic_data = PictureSeiralizer(pic_id, many=True).data
        return Response({"posts": pic_data}, status=status.HTTP_200_OK)


class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    # def post(self, request, id):
    # picture = Picture.objects.filter(id=id)
    def get(self, request, comment_id):
        print(comment_id)
        picture = Picture.objects.filter(id=comment_id)  # 이거 게시글 아이디임
        comments = Comment.objects.filter(picture__in=picture)
        serialized_data = CommentSerializer(comments, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request, comment_id):
        user = request.user
        request.data["user"] = user.id
        # request.data["picture"] = id
        request.data["picture"] = comment_id
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
