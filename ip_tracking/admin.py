from django.contrib import admin
from .models import RequestLog

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "path", "method", "timestamp")
    list_filter = ("method", "timestamp")
    search_fields = ("ip_address", "path")
