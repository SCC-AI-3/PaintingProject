from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import PictureSeiralizer, CommentSerializer
from .models import Picture, Comment
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers import UserSerializer


class PictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        picture = Picture.objects.all()
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
