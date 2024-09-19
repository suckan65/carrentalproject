from django.http import Http404, HttpResponse
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from imagess.models import Image
from imagess.api.serializers import ImageSerializer
from core import settings
import os
import mimetypes
from rest_framework.decorators import api_view


class UploadFileAPIView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    
    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response({
                "message": "Image upload success",
                "success": True,
                "imageId": str(file_serializer.data["id"])
            })
            
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ImageListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


def download_file(request, image_id):
    file = get_object_or_404(Image, id=image_id)
    
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image)) # http://127.0.0.1/media/images/araba1.jpg
    
    if not os.path.exists(file_path):
        raise Http404
    
    
    with open(file_path, "rb") as file_content:
        response = HttpResponse(file_content.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename=" + os.path.basename(file_path)
        
        return response
    


def display_image(request, image_id):
    file = get_object_or_404(Image, id=image_id)
    
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image)) # http://127.0.0.1/media/images/araba1.jpg

    if not os.path.exists(file_path):
        raise Http404
    
    file_name, file_ext = os.path.splitext(file_path)
    content_type, create = mimetypes.guess_type(file_ext)
    
    with open(file_path, "rb") as file_content:
        response = HttpResponse(file_content, content_type="image/jpeg")
        
        return response
    



@api_view(["DELETE"])
def delete_file(request, image_id):
    file = get_object_or_404(Image, id=image_id)
    
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image)) # http://127.0.0.1/media/images/araba1.jpg

    if not os.path.exists(file_path):
        raise Http404
    
    os.remove(file_path)
    file.delete()
    
    return Response({
        "message": "File and instance deleted successfully",
        "success": True
    })


