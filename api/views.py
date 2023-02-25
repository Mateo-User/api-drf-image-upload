from wsgiref.util import FileWrapper
from api.custom_renderers import JPEGRenderer, PNGRenderer
from rest_framework import generics, permissions, status
from images.models import Images
from .serializers import ImagesSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.decorators import renderer_classes, api_view
from django.http import HttpResponse
from .models import Image, UserAccount
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageSerializer, UserAccountSerializer


class ImageAPIView(generics.RetrieveAPIView):

    queryset = Images.objects.filter(id=1)
    renderer_classes = [JPEGRenderer]

    def get(self, request, *args, **kwargs):
        renderer_classes = [JPEGRenderer]
        queryset = Images.objects.get(id=self.kwargs['id']).image
        data = queryset
        return Response(data, content_type='image/jpg')
    
    
class ImageUploadView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image = image_serializer.save(user=request.user)
            return Response({
                'id': image.id,
                'image_thumbnail_200': image.image.url,
                'message': 'Image uploaded successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).order_by('-created_at')


class UserAccountView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserAccountSerializer

    def get_object(self):
        return UserAccount.objects.get(user=self.request.user)