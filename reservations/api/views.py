from reservations.models import Reservation
from reservations.api.serializers import ReservationSerialier
from core.page_filter import pages_filter
from rest_framework import generics, status, exceptions
from rest_framework.response import Response


class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerialier
    
    def post(self, request, format=None):
        user_id = None
        
        if request.path == "/reservations/add/auth/" or request.path == "/reservations/add/auth":
            user_id = request.query_params.get("userId")
            
        elif request.user.is_authenticated:
            user_id = request.user.id
            
        car_id = request.query_params.get("carId")
        
        
        if not user_id or not car_id:
            return Response({
                "error": "User ID and Car ID are required."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = request.data.copy()
        
        data["user_id"] = user_id
        
        data["car_id"] = car_id
        
        serializer = ReservationSerialier(data=data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Reservation created successfully",
                "success": True
            })
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ReservationAvailabilityAPIView(generics.GenericAPIView):
    serializer_class = ReservationSerialier
    
    def get(self, request, *args, **kwargs):
        car_id = self.request.query_params.get("carId")
        pick_up_date_time = self.request.query_params.get("pickUpDateTime")
        drop_off_date_time = self.request.query_params.get("dropOffDateTime")
        
        
        if not car_id or not pick_up_date_time or not drop_off_date_time:
            return Response({
                "error": "Car ID, Pick Up Date Time, and Drop Off Date Time parameters are required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
        reservations = Reservation.objects.filter(
            car_id=car_id,
            dropOffTime__gte=pick_up_date_time,
            pickUpTime__lte=drop_off_date_time
        )
        
        if reservations.exists():
            return Response({
                "message": "Car is not available for this time period"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({
                "message": "The car is available for this time period.",
                "success": True
            })
        


class ReservationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ReservationSerialier
    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        queryset = Reservation.objects.none()
        
        if not pk:
            raise exceptions.NotFound("There is no id in the URL")
        
        
        if self.request.path.endswith("/auth/"):
            user_id = self.request.user.id
            
            if not user_id:
                raise exceptions.PermissionDenied("User is not authenticated")
            
            queryset = Reservation.objects.filter(user_id=user_id)
            
            if not queryset:
                raise exceptions.NotFound("This user does not have any reservations in this id")
            
            return queryset
        
        
        if self.request.path.endswith("/admin/"):
            
            if self.request.user.is_staff:
                queryset = Reservation.objects.all()
                
            else:
                raise exceptions.NotFound("This user is not admin")
            
            return queryset
        
        
    def get(self, request, *args, **kwargs):
        
        try:
            queryset = self.get_queryset()
            
            if queryset is None:
                raise exceptions.NotFound("There is no reservation")
            
            
            return super().get(request, *args, **kwargs)
        
        except (exceptions.NotFound, exceptions.PermissionDenied) as e:
            return Response(str(e), status=e.status_code)



class ReservationListAll(generics.ListAPIView):
    serializer_class = ReservationSerialier
    
    def get_queryset(self):
        if self.request.path == "/reservations/admin/all/" and self.request.user.is_staff:
            return Reservation.objects.all()
        
        elif self.request.path == "/reservations/admin/all/" and not self.request.user.is_staff:
            return Reservation.objects.none()
        
        
        if self.request.user.is_staff:
            return Reservation.objects.all()
        
        elif self.request.user.is_authenticated:
            return Reservation.objects.filter(user_id=self.request.user.id)
        
        else:
            return Reservation.objects.none()
        
        
    def list(self, request, *args, **kwargs):
        
        if request.path == "/reservations/auth/all" and self.request.user.is_authenticated:
            return pages_filter(self, request, Reservation, *args, **kwargs)
        
        
        elif request.path == "/reservations/admin/auth/all" and self.request.user.is_staff:
            return pages_filter(self, request, Reservation, *args, **kwargs)
        
        elif request.path == "/reservations/admin/all/pages/" and self.request.user.is_staff:
            return pages_filter(self, request, Reservation, *args, **kwargs)
        
        
        return super().list(request, *args, **kwargs)
    



class ReservationDeleteAPIView(generics.DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerialier
    
    
    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            pk = self.kwargs["pk"]
            
            super().destroy(request, *args, **kwargs)
            
            return Response({
                "message": f"Reservation-{pk} is deleted successfully",
                "success": True
            })
        
        return Response({
            "message": "Only admin can delete reservations"
        },status=status.HTTP_401_UNAUTHORIZED)
    


class ReservationUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ReservationSerialier
    
    def put(self, request, *args, **kwargs):
        
        reserv_id = request.query_params.get("reservationId")
        car_id = request.query_params.get("carId")
        
        self.kwargs["pk"] = reserv_id
        
        if not reserv_id or not car_id:
            return Response({
                "error": "ID and Car ID are required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
        if request.user.is_staff:
            data = request.data.copy()
            
            data["id"] = reserv_id
            data["car_id"] = car_id
            
            instance = Reservation.objects.filter(id=reserv_id).first()
            
            serializer = ReservationSerialier(instance, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response({
                    "message": "The reservation has been updated successfully",
                    "success": True
                })
                
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({
                "message": "Only admin users can update reservations"
            }, status=status.HTTP_401_UNAUTHORIZED)

