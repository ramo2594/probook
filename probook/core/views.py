from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse

from .models import Professional
from .forms import BookingForm

from core.services.professional_service import ProfessionalService
from core.services.history_service import HistoryService
from core.services.booking_service import BookingService


@login_required
def my_dashboard(request):
    """Redirect alla dashboard del Professional collegato all'utente, o pagina informativa se manca."""
    professional = getattr(request.user, 'professional', None)
    if not professional:
        return render(request, 'core/no_professional.html')
    return redirect('professional_dashboard', professional_id=professional.id)


def home(request):
    """Home pubblica: mostra il primo Professional (per ora singolo salone/studio)."""
    professional = Professional.objects.first()
    return render(request, 'core/home.html', {'professional': professional})


@login_required
def professional_dashboard(request, professional_id):
    """Dashboard principale: dati presi da ProfessionalService."""
    professional = get_object_or_404(Professional, id=professional_id)
    stats = ProfessionalService.get_dashboard_stats(professional)
    return render(request, 'core/dashboard.html', {'professional': professional, **stats})


class ProfessionalLoginView(LoginView):
    """Login professionista con template custom e redirect alla propria dashboard."""
    template_name = 'registration/login.html'

    def get_success_url(self):
        professional = getattr(self.request.user, 'professional', None)
        return f'/dashboard/{professional.id}/' if professional else '/'


def public_booking(request, professional_id):
    """Form pubblico di prenotazione: delega creazione + email a BookingService."""
    professional = get_object_or_404(Professional, id=professional_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = BookingService.create_booking(professional_id, form)
            return redirect(reverse('booking_success', args=[booking.id]))
    else:
        form = BookingForm()

    return render(request, 'core/public_booking.html', {
        'professional': professional,
        'form': form,
    })


def booking_success(request, booking_id):
    """Pagina di conferma dopo l'invio della prenotazione."""
    booking = get_object_or_404(Professional._meta.model._meta.apps.get_model('core', 'Booking'), id=booking_id)
    return render(request, 'core/booking_success.html', {'booking': booking})


@login_required
def booking_history(request):
    """Storico prenotazioni del professionista loggato (gestito da HistoryService)."""
    professional = Professional.objects.get(user=request.user)
    bookings = HistoryService.get_professional_history(professional)
    return render(request, 'core/booking_history.html', {
        'professional': professional,
        'bookings': bookings,
    })
