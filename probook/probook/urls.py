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
    # Admin Django
    path('admin/', admin.site.urls),

    # Dashboard professionista
    path('dashboard/me/', core_views.my_dashboard, name='my_dashboard'),
    path('dashboard/<int:professional_id>/', core_views.professional_dashboard, name='professional_dashboard'),
    path('dashboard/history/', booking_history, name='booking_history'),

    # Prenotazioni pubbliche
    path('book/<int:professional_id>/', core_views.public_booking, name='public_booking'),
    path('booking/success/<int:booking_id>/', core_views.booking_success, name='booking_success'),

    # Auth built‑in (login/logout/password reset ecc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Home pubblica
    path('', core_views.home, name='home'),
]
