from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="images/")
    size = models.IntegerField(default=1024, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"