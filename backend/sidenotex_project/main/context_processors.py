from .models import CustomUser

def user_domain(request):
    if 'user_id' in request.session:
        try:
            user = CustomUser.objects.get(id=request.session['user_id'])
            return {'user_domain': user.user_domain}
        except CustomUser.DoesNotExist:
            pass
    return {'user_domain': None}