from django.contrib import admin
from imagess.models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "size", "type"]
    list_display_links = ["name"]
