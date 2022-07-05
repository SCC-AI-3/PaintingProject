from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import PictureSeiralizer
from .models import Picture
from rest_framework_simplejwt.authentication import JWTAuthentication

class PictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
            Picture_serializer.save()

            return Response({"message": "정상"}, status=status.HTTP_200_OK)

        return Response(Picture_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        picture = Picture.objects.get(id=obj_id)

        Picture_serializer = PictureSeiralizer(picture, data=request.data, partial=True)
        if Picture_serializer.is_valid():
            Picture_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        return Response(Picture_serializer.errors, status=status.HTTP_400_BAD_REQUEST)