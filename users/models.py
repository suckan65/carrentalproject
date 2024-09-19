from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group, Permission


class User(BaseUser):
    phone_regex = RegexValidator(
        regex=r"^\(\d{3}\) \d{3}-\d{4}$",
        message="Phone number must be entered in the format: (999) 999-9999"
    )
    
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    phoneNumber = models.CharField(validators=[phone_regex], max_length=14)
    address = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=15)
    builtIn = models.BooleanField(default=False)
    roles = models.CharField(max_length=100)
    confirmPassword = models.CharField(max_length=30)
    
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_set_permissions", blank=True)
    
    objects = BaseUserManager()
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"