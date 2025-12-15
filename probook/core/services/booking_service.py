from django.core.mail import send_mail
from core.models import Booking, Professional


class BookingService:
    @staticmethod
    def create_booking(professional_id, form):
        """
        Logica estratta da public_booking:
        - crea la Booking collegata al Professional
        - invia email a professionista e cliente
        - restituisce l'oggetto booking
        """
        professional = Professional.objects.get(id=professional_id)

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
            fail_silently=True,
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

        return booking
