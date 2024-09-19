from rest_framework import serializers
from reservations.models import Reservation
from cars.models import Car
from cars.api.serializers import CarSerializer
from decimal import Decimal
from dateutil import parser
from datetime import datetime, timezone


class ReservationSerialier(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    
    car_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    userId = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = ("id", "car", "pickUpTime", "dropOffTime", "car_id", "user_id",
                  "pickUpLocation", "dropOffLocation", "status", "totalPrice", "userId")
        
        extra_kwargs = {
            "totalPrice": {
                "read_only": True
            },
            "status": {
                "read_only": True
            }
        }
        
        
    def get_userId(self, obj):
        return obj.user.id
        
        
    def validate_pickUpTime(self, value):
            
        if value <= datetime.now(timezone.utc):
            raise serializers.ValidationError("Pick-up time must be in the future.")
            
        return value
        
        
    def validate_dropOffTime(self, value):
            
        pick_up_time = self.initial_data.get("pickUpTime")
            
        if pick_up_time is None:
            raise serializers.ValidationError("Pick-up time must be provided")
            
        pick_up_time_parsed = parser.parse(pick_up_time).replace(tzinfo=timezone.utc)
            
        if value <= pick_up_time_parsed:
            raise serializers.ValidationError("Drop-off time must be later than pick-up time")
            
        return value
        
        
    def validate(self, attrs):
        pick_up_time = attrs["pickUpTime"]
        drop_off_time = attrs["dropOffTime"]
        car_id = attrs["car_id"]
            
            
        overlapping_reservations = Reservation.objects.filter(
            car_id=Car.objects.get(id=car_id),
            pickUpTime__lt=drop_off_time,
            dropOffTime__gt=pick_up_time
        )
            
        if self.instance:
            overlapping_reservations = overlapping_reservations.exclude(pk=self.instance.pk)
                
        if overlapping_reservations.exists():
            raise serializers.ValidationError("Reservation overlaps with existing resevations")
            
            
        return attrs
        
        
    def create(self, validated_data):
        try:
            car_id = validated_data["car_id"]
            car = Car.objects.get(id=car_id)
            pick_up_time = validated_data["pickUpTime"]
            drop_off_time = validated_data["dropOffTime"]
            price_per_hour = float(car.pricePerHour)
                
            total_hours = (drop_off_time - pick_up_time).total_seconds() / 3600
                
            total_price = Decimal(total_hours) * Decimal(price_per_hour)
                
            validated_data["totalPrice"] = total_price
                
            return super().create(validated_data)
            
        except Exception as e:
            raise serializers.ValidationError(f"{e}")
            
            
            
    def update(self, instance, validated_data):
        
        car_id = validated_data["car_id"]
        car = Car.objects.get(id=car_id)
        pick_up_time = validated_data["pickUpTime"]
        drop_off_time = validated_data["dropOffTime"]
        price_per_hour = float(car.pricePerHour)
        
        total_hours = (drop_off_time - pick_up_time).total_seconds() / 3600
                
        total_price = Decimal(total_hours) * Decimal(price_per_hour)
                
        validated_data["totalPrice"] = total_price
        
        return super().update(instance, validated_data)