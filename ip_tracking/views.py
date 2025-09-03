from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def dynamic_rate_limit(request):
    """Return rate limit string depending on authentication status."""
    return "10/m" if request.user.is_authenticated else "5/m"

# Safe root view
@csrf_exempt
def home_view(request):
    return HttpResponse("Hello, world!")

@csrf_exempt
def favicon_view(request):
    return HttpResponse(status=204)  # empty response

# Login view with dynamic rate limiting
@csrf_exempt
def login_view(request):
    # Only apply ratelimit to POST requests
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    # Dynamically wrap the inner function
    @ratelimit(key='ip', rate=dynamic_rate_limit(request), method='POST', block=True)
    def inner(req):
        return JsonResponse({"message": "Login endpoint accessed"})

    return inner(request)

# GraphQL view
@csrf_exempt
def graphql_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        query = data.get("query", "")
        # Here you would execute the GraphQL query
        return JsonResponse({"query_received": query})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
