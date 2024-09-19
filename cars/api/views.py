from cars.models import Car
from cars.api.serializers import CarSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from core.page_filter import pages_filter


class CarAddAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    
    def create(self, request, *args, **kwargs):
        super().create(request,*args, **kwargs)
        
        return Response({
            "message": "Car created successfully",
            "success": True
        })
    
class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    
    
    def list(self, request, *args, **kwargs):
        if request.path.startswith("/car/visitors/pages/") or request.path.startswith("/car/visitors/pages"):
            return pages_filter(self, request, Car, *args, **kwargs)
        
        return super().list(request, *args, **kwargs)
    

class CarDeleteAPIView(generics.DestroyAPIView):
    queryset = Car.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        
        return Response({
            "message": "Car deleted successfully",
            "success": True
        })
    

class CarUpdateAPIView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        car_id = request.query_params.get("id")
        image_id = request.query_params.get("imageId")
        
        
        if car_id is None:
            return Response({
                "detail": "Car ID is missing in the request"
            })
            
            
        try:
            car = Car.objects.get(id=car_id)
            
        except Car.DoesNotExist:
            return Response({
                "detail": "Car not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        
        
        cleaned_data = {key: value for key, value in request.data.items() if value is not None}
        
        serializer = self.get_serializer(instance=car, data=cleaned_data, partial=partial)
        
        
        if serializer.is_valid():
            if not image_id:
                serializer.validated_data["image"] = []
                
            serializer.save()
            
            return Response({
                "message": "Car updated successfully",
                "success": True
            })
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)