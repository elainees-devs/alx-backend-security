from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import IPLog

@admin.register(IPLog)
class IPLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "path", "method", "timestamp")
    list_filter = ("method", "timestamp")
    search_fields = ("ip_address", "path")
