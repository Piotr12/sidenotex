# main/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import CustomUser
from django.http import HttpResponse
from django.core.mail import send_mail
import uuid
from .decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Sidenote
from .forms import SidenoteForm  # We'll create this
from django.contrib import messages
from django.conf import settings


def landing_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ip = get_client_ip(request)
        user, created = CustomUser.objects.get_or_create(email=email, defaults={
            'token': uuid.uuid4().hex,
            'created_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_ip': ip,
        })
        try:
            # Try sending mail

            print(f"Email settings check:")
            print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            print(f"EMAIL_HOST_PASSWORD length: {len(settings.EMAIL_HOST_PASSWORD)}")
           
            send_mail(
                'Your sidenotex Token',
                f'Your login token is: {user.token}',
                'contact@sidenotex.com',
                [email],
                fail_silently=False
            )
            print("Email sent successfully")
        except Exception as e:
            import traceback
            print(f"Error sending email: {str(e)}")
            print("Full traceback:")
            print(traceback.format_exc())
            return HttpResponse(f"Error sending email: {str(e)}", status=500)
            
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
    sidenotes = Sidenote.objects.filter(author=user).order_by('-created_at')
    
    if request.method == 'POST':
        form = SidenoteForm(request.POST)
        if form.is_valid():
            sidenote = form.save(commit=False)
            sidenote.author = user
            sidenote.save()
            messages.success(request, 'Sidenote added successfully!')
            return redirect('dashboard')
    else:
        form = SidenoteForm()

    return render(request, 'dashboard.html', {
        'email': user.email,
        'user_domain': user.user_domain,
        'sidenotes': sidenotes,
        'form': form
    })

@login_required
def delete_sidenote(request, pk):
    sidenote = get_object_or_404(Sidenote, pk=pk, author_id=request.session['user_id'])
    sidenote.delete()
    messages.success(request, 'Sidenote deleted successfully!')
    return redirect('dashboard')

@login_required
def edit_sidenote(request, pk):
    sidenote = get_object_or_404(Sidenote, pk=pk, author_id=request.session['user_id'])
    
    if request.method == 'POST':
        form = SidenoteForm(request.POST, instance=sidenote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sidenote updated successfully!')
            return redirect('dashboard')
    else:
        form = SidenoteForm(instance=sidenote)
    
    return render(request, 'edit_sidenote.html', {'form': form})


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