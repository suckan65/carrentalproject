from django.urls import path
from excel import views

urlpatterns = [
    path("download/users/", views.export_excel_users, name="users-excel"),
    # path("download/users/", views.export_user_xlsx, name="users-excel"),
    path("download/cars/", views.export_excel_cars, name="cars-excel"),
    path("download/reservations/", views.export_excel_reservations, name="reservations-excel"),
]