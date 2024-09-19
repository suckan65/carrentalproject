from django.urls import path
from imagess.api import views

urlpatterns = [
    path("upload/", views.UploadFileAPIView.as_view(), name="upload-image"),
    path("", views.ImageListAPIView.as_view(), name="list-images"),
    path("download/<int:image_id>/", views.download_file, name="image-download"),
    path("display/<int:image_id>/", views.display_image, name="image-display"),
    path("<int:image_id>/", views.delete_file, name="image-delete"),
]