from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse

def dynamic_rate_limit(request):
    """
    Return rate limit string depending on authentication status.
    """
    if request.user.is_authenticated:
        return "10/m"
    return "5/m"

def login_view(request):
    """
    Login view with dynamic rate limiting:
    - 10 requests/min for authenticated users
    - 5 requests/min for anonymous users
    """
    # Apply rate limiting manually
    limiter = ratelimit(key='ip', rate=dynamic_rate_limit(request), method='POST', block=True)
    return limiter(lambda req: JsonResponse({"message": "Login endpoint accessed"}))(request)

