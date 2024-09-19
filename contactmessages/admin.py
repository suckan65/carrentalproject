from django.contrib import admin
from contactmessages.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "subjects", "email"]
    list_display_links = ["name"]
