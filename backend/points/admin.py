from django.contrib import admin
from .models import Point


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'author', 'created_at')
