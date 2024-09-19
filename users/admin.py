from django.contrib import admin
from users.models import User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "firstName", "lastName", "phoneNumber"]
    list_display_links = ["email"]