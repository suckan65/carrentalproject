from django.db import models



class Message(models.Model):
    name = models.CharField(max_length=50)
    subjects = models.CharField(max_length=50)
    body = models.TextField(max_length=500)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.name}"