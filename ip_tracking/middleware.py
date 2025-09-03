from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from django.core.cache import cache
import ipinfo
from django.conf import settings

class IPLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log IP address, path, method, and geolocation safely.
    """

    SKIP_PATHS = ["/favicon.ico", "/", "/robots.txt"]

    def process_request(self, request):
        path = request.path

        # Skip homepage, favicon, robots, and well-known paths
        if path in self.SKIP_PATHS or path.startswith("/.well-known/"):
            return

        ip = self.get_client_ip(request)
        if not ip:
            return  # skip if IP not found

        # Blocked IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Forbidden: Your IP is blocked.")

        # Geolocation caching with try/except
        cache_key = f"geo_{ip}"
        geo_data = cache.get(cache_key)
        if not geo_data:
            try:
                handler = ipinfo.getHandler(settings.IPINFO_ACCESS_TOKEN)
                details = handler.getDetails(ip)
                geo_data = {"country_name": details.country_name, "city": details.city}
                cache.set(cache_key, geo_data, 60*60*24)
            except Exception:
                geo_data = {"country_name": None, "city": None}

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            method=request.method,
            country=geo_data.get("country_name"),
            city=geo_data.get("city")
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
