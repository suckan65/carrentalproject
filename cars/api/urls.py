from django.urls import path
from cars.api import views

urlpatterns = [
    path("admin/<int:imageId>/add/", views.CarAddAPIView.as_view(), name="car-add"),
    path("visitors/<int:pk>/", views.CarDetailAPIView.as_view(), name="car-detail"),
    path("visitors/pages/", views.CarListAPIView.as_view(), name="car-all-pages"),
    path("visitors/all/", views.CarListAPIView.as_view(), name="car-all"),
    path("admin/<int:pk>/auth/", views.CarDeleteAPIView.as_view(), name="car-delete"),
    path("admin/auth/", views.CarUpdateAPIView.as_view(), name="car-update"),
]
