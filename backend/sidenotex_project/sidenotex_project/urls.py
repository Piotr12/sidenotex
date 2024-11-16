# sidenotex_project/urls.py

from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from main import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('account_created/', views.account_created, name='account_created'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('sidenote/<int:pk>/edit/', views.edit_sidenote, name='edit_sidenote'),
    path('sidenote/<int:pk>/delete/', views.delete_sidenote, name='delete_sidenote'),
    path('api/sidenotes/', api_views.list_sidenotes, name='api_list_sidenotes'),
    path('api/sidenotes/create/', api_views.create_sidenote, name='api_create_sidenote'),
    path('login/<str:token>/', views.direct_login, name='direct_login'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('terms/', views.terms, name='terms'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)