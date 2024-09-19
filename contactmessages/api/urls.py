from django.urls import path
from contactmessages.api import views

urlpatterns = [
    path("visitors/", views.MessageCreateAPIView.as_view(), name="message-create"),
    path("", views.MessageListAPIView.as_view(), name="list-all-messages"),
    path("request/", views.MessageListAPIView.as_view(), name="list-request-messages"),
    path("pages/", views.MessageListAPIView.as_view(), name="list-pages-messages"),
    path("<int:pk>/", views.MessageDetailAPIView.as_view(), name="message-detail"),
]