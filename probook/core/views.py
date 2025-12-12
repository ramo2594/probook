from datetime import date
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.core.mail import send_mail

from .models import Professional, Booking
from .forms import BookingForm


@login_required
def my_dashboard(request):
    """
    View di comodo:
    - trova il Professional collegato all'utente loggato
    - lo reindirizza automaticamente alla sua dashboard /dashboard/<id>/
    Se l'utente non ha un profilo Professional collegato, mostra una pagina dedicata.
    """
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        # Utente loggato ma senza profilo professional: niente dashboard, solo messaggio esplicativo
        return render(request, 'core/no_professional.html')

    # Redirect permanente alla dashboard specifica del professionista
    return redirect('professional_dashboard', professional_id=professional.id)


def home(request):
    """
    Home pubblica del sito:
    - recupera il primo Professional presente (per ora assumiamo un solo salone/studio)
    - mostra i pulsanti "Prenota" e "Login professionista".
    In futuro si può estendere a multi‑salone.
    """
    professional = Professional.objects.first()
    context = {
        'professional': professional,
    }
    return render(request, 'core/home.html', context)


@login_required
def professional_dashboard(request, professional_id):
    """
    Dashboard principale del professionista.
    Mostra:
    - prenotazioni future (oggi e oltre)
    - conteggio prenotazioni future
    - conteggio prenotazioni di oggi
    - prossima prenotazione in agenda
    - totale prenotazioni registrate (per le card in alto).
    """
    professional = get_object_or_404(Professional, id=professional_id)

    today = date.today()
    now = timezone.localtime().time()

    # Tutte le prenotazioni del professionista, ordinate cronologicamente
    all_bookings = Booking.objects.filter(
        professional=professional
    ).order_by('date', 'time')
    total_bookings = all_bookings.count()

    # Prenotazioni future (usate nella tabella principale della dashboard)
    future_bookings = all_bookings.filter(date__gte=today)

    # Prenotazioni di oggi (per la card "Prenotazioni di oggi")
    todays_bookings = all_bookings.filter(date=today)

    # Prossima prenotazione:
    # - prima cerco oggi, a partire dall'ora corrente
    # - se non c'è nulla oggi, prendo la prima dei giorni successivi
    next_booking = future_bookings.filter(
        date=today, time__gte=now
    ).first() or future_bookings.filter(
        date__gt=today
    ).first()

    context = {
        'professional': professional,
        'bookings': future_bookings,        # usate nella tabella "Prenotazioni in arrivo"
        'future_count': future_bookings.count(),
        'today_count': todays_bookings.count(),
        'next_booking': next_booking,
        'total_bookings': total_bookings,
    }
    return render(request, 'core/dashboard.html', context)


class ProfessionalLoginView(LoginView):
    """
    Vista di login per i professionisti che usa il template custom.
    Riutilizza tutta la logica di LoginView di Django, cambiando solo:
    - template_name
    - redirect dopo il login (get_success_url).
    """
    template_name = 'registration/login.html'

    def get_success_url(self):
        """
        Dopo il login:
        - se l'utente ha un Professional collegato, lo porta alla sua dashboard /dashboard/<id>/
        - altrimenti, come fallback, lo rimanda alla home.
        """
        professional = getattr(self.request.user, 'professional', None)
        if professional:
            return f'/dashboard/{professional.id}/'
        return '/'


def public_booking(request, professional_id):
    """
    Form pubblico di prenotazione per un determinato Professional.
    Flusso:
    - GET: mostra il form vuoto
    - POST valido: crea la Booking, invia due email (professionista + cliente)
      e reindirizza alla pagina di conferma.
    """
    professional = get_object_or_404(Professional, id=professional_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Creo la prenotazione collegandola al professional corrente
            booking = form.save(commit=False)
            booking.professional = professional
            booking.save()

            # Email di notifica al professionista
            subject = f"Nuova prenotazione per {professional.business_name}"
            message = (
                f"Hai una nuova prenotazione.\n\n"
                f"Cliente: {booking.client_name} ({booking.client_email})\n"
                f"Servizio: {booking.service}\n"
                f"Data: {booking.date} alle {booking.time}\n"
            )
            send_mail(
                subject,
                message,
                None,  # usa DEFAULT_FROM_EMAIL dalle settings
                [professional.user.email],
                fail_silently=True,  # in produzione si può togliere per vedere eventuali errori
            )

            # Email di conferma al cliente
            subject_client = f"Conferma prenotazione da {professional.business_name}"
            message_client = (
                f"Ciao {booking.client_name},\n\n"
                f"la tua prenotazione è confermata per il {booking.date} alle {booking.time}.\n"
                f"Servizio: {booking.service}\n"
                f"Professionista: {professional.business_name}\n"
            )
            send_mail(
                subject_client,
                message_client,
                None,
                [booking.client_email],
                fail_silently=True,
            )

            # Redirect alla pagina di conferma dedicata
            return redirect(reverse('booking_success', args=[booking.id]))
    else:
        # Primo accesso: form vuoto
        form = BookingForm()

    context = {
        'professional': professional,
        'form': form,
    }
    return render(request, 'core/public_booking.html', context)


def booking_success(request, booking_id):
    """
    Pagina di conferma mostrata dopo l'invio della prenotazione.
    Riporta i dettagli dell'appuntamento appena creato.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'core/booking_success.html', {'booking': booking})


@login_required
def booking_history(request):
    """
    Storico completo delle prenotazioni del professionista loggato.
    Mostra tutte le booking (passate e future) ordinate dalla più recente alla più vecchia.
    """
    professional = Professional.objects.get(user=request.user)
    bookings = Booking.objects.filter(
        professional=professional
    ).order_by('-date', '-time')  # più recenti in alto

    return render(request, 'core/booking_history.html', {
        'professional': professional,
        'bookings': bookings,
    })
