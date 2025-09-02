from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from django.core.cache import cache
import ipinfo
from django.conf import settings

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path

        # Block IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Forbidden: Your IP is blocked.")

        # Geolocation caching
        cache_key = f"geo_{ip}"
        geo_data = cache.get(cache_key)
        if not geo_data:
            handler = ipinfo.getHandler(settings.IPINFO_ACCESS_TOKEN)
            details = handler.getDetails(ip)
            geo_data = {
                "country_name": details.country_name,
                "city": details.city
            }
            cache.set(cache_key, geo_data, 60 * 60 * 24)  # cache 24 hours

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            country=geo_data.get("country_name"),
            city=geo_data.get("city")
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
