from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, Sidenote

def get_user_from_token(token):
    try:
        return CustomUser.objects.get(token=token)
    except CustomUser.DoesNotExist:
        return None

@csrf_exempt
@require_http_methods(["GET"])
def list_sidenotes(request):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Token '):
        return JsonResponse({'error': 'Invalid authorization header'}, status=401)
    
    token = auth_header.split(' ')[1]
    user = get_user_from_token(token)
    if not user:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # Get URL from query parameters
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'URL parameter is required'}, status=400)

    # Filter sidenotes by domain and URL, order by created_at descending, limit to 6
    sidenotes = Sidenote.objects.filter(
        domain=user.user_domain,
        url=url
    ).order_by('-created_at')[:6].values('text', 'created_at', 'author__name')

    return JsonResponse({'sidenotes': list(sidenotes)})

@csrf_exempt
@require_http_methods(["POST"])
def create_sidenote(request):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Token '):
        return JsonResponse({'error': 'Invalid authorization header'}, status=401)
    
    token = auth_header.split(' ')[1]
    user = get_user_from_token(token)
    if not user:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    try:
        data = json.loads(request.body)
        url = data.get('url')
        text = data.get('text')

        if not url or not text:
            return JsonResponse({'error': 'URL and text are required'}, status=400)

        sidenote = Sidenote.objects.create(
            url=url,
            text=text,
            author=user,
            domain=user.user_domain
        )

        return JsonResponse({
            'id': sidenote.id,
            'url': sidenote.url,
            'text': sidenote.text,
            'created_at': sidenote.created_at
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)