from rest_framework import generics
from contactmessages.models import Message
from contactmessages.api.serializers import MessageSerializer
from rest_framework.response import Response
from core.page_filter import pages_filter

class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            "message": "Successfully created message",
            "success": True
        })
    

class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        if self.request.path == "/contactmessage/request/" or self.request.path == "/contactmessage/request":
            return Message.objects.filter(pk=self.request.query_params.get("id"))
        return Message.objects.all()
    
    def list(self, request, *args, **kwargs):
        if self.request.path == "/contactmessage/pages/" or self.request.path == "/contactmessage/pages":
            return pages_filter(self, request, Message, *args, **kwargs)
        
        return super().list(request, *args, **kwargs)
    

class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    