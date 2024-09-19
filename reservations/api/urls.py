from django.urls import path
from reservations.api import views


urlpatterns = [
    path("add/auth/", views.ReservationCreateAPIView.as_view(), name="car-user-add-reserv"),
    path("add/", views.ReservationCreateAPIView.as_view(), name="car-add-reserv"),
    path("auth/", views.ReservationAvailabilityAPIView.as_view(), name="reserv-availability"),
    path("<int:pk>/auth/", views.ReservationDetailAPIView.as_view(), name="reserv-detail-auth"),
    path("<int:pk>/admin/", views.ReservationDetailAPIView.as_view(), name="reserv-detail-admin"),
    path("admin/all/", views.ReservationListAll.as_view(), name="list-admin-all"),
    path("auth/all/", views.ReservationListAll.as_view(), name="list-auth-all"),
    path("admin/auth/all/", views.ReservationListAll.as_view(), name="list-admin-auth-all"),
    path("admin/all/pages/", views.ReservationListAll.as_view(), name="list-admin-pages-all"),
    path("admin/<int:pk>/auth/", views.ReservationDeleteAPIView.as_view(), name="reserv-delete"),
    path("admin/auth/", views.ReservationUpdateAPIView.as_view(), name="reserv_update"),
]