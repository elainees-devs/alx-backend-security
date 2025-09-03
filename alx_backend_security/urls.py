from django.contrib import admin
from django.urls import path, include
from ip_tracking.views import home_view, favicon_view

urlpatterns = [
    path('admin/', admin.site.urls),               # Admin panel
    path('', home_view, name='home'),             # Root URL
    path('favicon.ico', favicon_view, name='favicon'), # Favicon
    path('api/', include('ip_tracking.urls')),    # Include app URLs
]
