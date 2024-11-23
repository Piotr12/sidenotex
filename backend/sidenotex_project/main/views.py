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
from django.core.paginator import Paginator
from urllib.parse import unquote, quote
from django.db.models import Q
from hashlib import sha256
import os



def landing_page(request):
    if 'user_id' in request.session:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        ip = get_client_ip(request)
        
        # Extract domain from email before hashing
        user_domain = email.split('@')[1].lower()
        
        # Create a hash of the email
        email_hash = sha256(email.lower().encode()).hexdigest()
        
        # Use the email hash instead of email for user lookup/creation
        user, created = CustomUser.objects.get_or_create(email_hash=email_hash, defaults={
            'token': uuid.uuid4().hex,
            'created_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_ip': ip,
            'user_domain': user_domain,  # Set the domain here
        })
        try:
            # Try sending mail

           
            html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Welcome to sidenotex!</h2>
                        
                        <p>Thank you for signing up. Click the button below to log in:</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="https://sidenotex.com/login/{user.token}" 
                            style="background-color: #2563eb; color: white; padding: 12px 24px; 
                                    text-decoration: none; border-radius: 6px; font-weight: 500;">
                                Log In to sidenotex
                            </a>
                        </div>

                        <p style="margin-top: 30px;">Or copy your login token below and use it at <a href="https://sidenotex.com/login">sidenotex.com/login</a>:</p>
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; 
                                    font-family: monospace; font-size: 18px;">
                            {user.token}
                        </div>

                        <p style="color: #7f8c8d; font-size: 14px; margin-top: 30px;">
                            For security reasons, please keep this token private. If you didn't request this email, please ignore it.
                        </p>
                    </div>
                </body>
                </html>
                """

            send_mail(
                'Welcome to sidenotex - Your Login Token',
                f'Your login token is: {user.token}\nVisit https://sidenotex.com/login to log in.',  # Plain text version
                'contact@sidenotex.com',
                [email],
                fail_silently=False,
                html_message=html_content
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

def direct_login(request, token):
    try:
        user = CustomUser.objects.get(token=token)
        request.session['user_id'] = user.id
        return redirect('dashboard')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid or expired token')
        return redirect('login')

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
    
    if request.method == 'POST':
        if 'update_name' in request.POST:  # New name update handling
            new_name = request.POST.get('name', '').strip()
            if new_name:
                user.name = new_name
                user.save()
                messages.success(request, 'Name updated successfully!')
            return redirect('dashboard')
        form = SidenoteForm(request.POST)

        if form.is_valid():
            sidenote = form.save(commit=False)
            sidenote.author = user
            sidenote.save()
            messages.success(request, 'Sidenote added successfully!')
            return redirect('dashboard')
    else:
        form = SidenoteForm()
    
    sidenotes = Sidenote.objects.filter(author=user).order_by('-created_at')
    
    return render(request, 'dashboard.html', {
        'email': user.email_hash,
        'user_name': user.name,  # Add name to context
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

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.session['user_id'])
        user.delete()  # This will also delete all associated sidenotes due to CASCADE
        request.session.flush()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('landing_page')
    return redirect('dashboard')

def terms(request):
    return render(request, 'terms.html')

@login_required
def url_sidenotes(request):
    search_url = unquote(request.GET.get('url', ''))
    page_number = request.GET.get('p', 1)
    user = CustomUser.objects.get(id=request.session['user_id'])
    
    sidenotes = None
    if search_url:
        # Create URL variants (with and without trailing slash)
        url_with_slash = search_url if search_url.endswith('/') else f"{search_url}/"
        url_without_slash = search_url[:-1] if search_url.endswith('/') else search_url
        
        sidenotes_list = Sidenote.objects.filter(
            Q(url=url_with_slash) | Q(url=url_without_slash),
            domain=user.user_domain
        ).order_by('-created_at')
        
        paginator = Paginator(sidenotes_list, 10)
        try:
            sidenotes = paginator.page(page_number)
        except (ValueError, TypeError):
            sidenotes = paginator.page(1)
    
    return render(request, 'url_sidenotes.html', {
        'search_url': search_url,
        'encoded_url': quote(search_url) if search_url else '',
        'sidenotes': sidenotes,
    })

def about(request):
    return render(request, 'about.html')

def prompts(request):
    prompts_dir = os.path.join(settings.STATIC_ROOT, 'prompts')
    prompts_list = []
    selected_prompt = None
    
    try:
        # Get all .md files and sort them alphabetically
        files = sorted([f for f in os.listdir(prompts_dir) if f.endswith('.md')])
        
        # Create list of all prompts
        prompts_list = [{'filename': f, 'title': f.replace('.md', '')} for f in files]
        
        # Handle selected prompt
        selected_filename = request.GET.get('prompt')
        if selected_filename:
            file_path = os.path.join(prompts_dir, selected_filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    selected_prompt = {
                        'title': selected_filename.replace('.md', ''),
                        'content': file.read()
                    }
                    
    except FileNotFoundError:
        prompts_list = []
        
    return render(request, 'prompts.html', {
        'prompts': prompts_list,
        'selected_prompt': selected_prompt
    })