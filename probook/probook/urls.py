"""
URL configuration for probook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from core.views import ProfessionalLoginView, booking_history  

urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/me/', core_views.my_dashboard, name='my_dashboard'),
    path('dashboard/<int:professional_id>/', core_views.professional_dashboard, name='professional_dashboard'),

    path('dashboard/history/', booking_history, name='booking_history'),

    path('book/<int:professional_id>/', core_views.public_booking, name='public_booking'),
    path('booking/success/<int:booking_id>/', core_views.booking_success, name='booking_success'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('', core_views.home, name='home'),
    
]

