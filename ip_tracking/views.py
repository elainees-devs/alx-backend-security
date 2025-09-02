from django_ratelimit.decorators import ratelimit

from django.http import JsonResponse

@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def login_view(request):
    return JsonResponse({"message": "Login endpoint accessed"})
