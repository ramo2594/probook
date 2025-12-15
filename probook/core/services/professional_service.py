from datetime import date
from django.utils import timezone
from core.models import Booking


class ProfessionalService:
    @staticmethod
    def get_dashboard_stats(professional):
        """
        Dashboard principale del professionista.
        Mostra:
        - prenotazioni future (oggi e oltre)
        - conteggio prenotazioni future
        - conteggio prenotazioni di oggi
        - prossima prenotazione in agenda
        - totale prenotazioni registrate (per le card in alto).
        """
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

        return {
            'bookings': future_bookings,        # usate nella tabella "Prenotazioni in arrivo"
            'future_count': future_bookings.count(),
            'today_count': todays_bookings.count(),
            'next_booking': next_booking,
            'total_bookings': total_bookings,
        }
