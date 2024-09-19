from django.db import models


TRANSMISSION = (
    ("a", "Automatic"),
    ("m", "Manual"),
    ("t", "Triptonic")
)

FUEL = (
    ("g", "Gasoline"),
    ("d", "Diesel"),
    ("e", "Electricity"),
    ("h", "Hybrid"),
    ("hy", "Hydrogen"),
    ("l", "LPG"),
    ("c", "CNG")
)



class Car(models.Model):
    model = models.CharField(max_length=100)
    doors = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    luggage = models.PositiveIntegerField()
    transmission = models.CharField(max_length=10, choices=TRANSMISSION)
    airConditioning = models.BooleanField()
    age = models.PositiveIntegerField()
    pricePerHour = models.DecimalField(max_digits=8, decimal_places=2)
    fuelType = models.CharField(max_length=2, choices=FUEL)
    builtIn = models.BooleanField(default=True)
    image = models.CharField(max_length=30, blank=True, null=True)

    
    def __str__(self):
        return f"{self.model}"


