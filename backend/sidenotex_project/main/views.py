# main/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import CustomUser
from django.http import HttpResponse
from django.core.mail import send_mail
import uuid
from .decorators import login_required

def landing_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ip = get_client_ip(request)
        user, created = CustomUser.objects.get_or_create(email=email, defaults={
            'token': uuid.uuid4().hex,
            'created_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_ip': ip,
        })
        # Send email with the token
        send_mail(
            'Your sidenotex Token',
            f'Your login token is: {user.token}',
            'no-reply@sidenotex.com',
            [email],
        )
        return redirect('account_created')
    return render(request, 'landing_page.html')

def account_created(request):
    return render(request, 'account_created.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_view(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            user = CustomUser.objects.get(token=token)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        except CustomUser.DoesNotExist:
            return HttpResponse('Invalid token', status=401)
    return render(request, 'login.html')


@login_required
def dashboard(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    return render(request, 'dashboard.html', {
        'email': user.email,
        'user_domain': user.user_domain
    })

def login_view(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            user = CustomUser.objects.get(token=token)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        except CustomUser.DoesNotExist:
            return HttpResponse('Invalid token', status=401)
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('landing_page')