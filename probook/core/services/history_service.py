from core.models import Booking


class HistoryService:
    @staticmethod
    def get_professional_history(professional):
        """
        Storico completo delle prenotazioni del professionista loggato.
        Mostra tutte le booking (passate e future) ordinate dalla più recente alla più vecchia.
        """
        return Booking.objects.filter(
            professional=professional
        ).order_by('-date', '-time')  # più recenti in alto
