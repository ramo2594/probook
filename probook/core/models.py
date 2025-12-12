from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modello utente personalizzato che estende l'AbstractUser standard di Django.
    Aggiungo:
    - is_professional: flag per capire se l'utente è anche un professionista
      che può avere una dashboard e prenotazioni collegate.
    - phone: numero di telefono opzionale, utile per contatti rapidi.
    """
    is_professional = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # Rappresentazione leggibile dell'utente (es. in admin e shell)
        return self.username


class Professional(models.Model):
    """
    Profilo del professionista (salone/studio) collegato 1‑a‑1 a un User.
    Qui vivo tutte le info del business, separandole dal semplice account utente.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,     # Se cancello l'utente, sparisce anche il profilo Professional
        related_name='professional',  # Permette di fare request.user.professional
    )
    business_name = models.CharField(max_length=200)  # Nome commerciale del salone/studio
    services = models.TextField(
        blank=True,
        help_text="Descrizione libera dei servizi offerti (es. 'Taglio, Barba, Colore').",
    )

    def __str__(self):
        # Mostro il nome del salone/studio ovunque serva una stringa
        return self.business_name


class Booking(models.Model):
    """
    Singola prenotazione effettuata da un cliente per un determinato Professional.
    Raccoglie i dati minimi per gestire appuntamenti e storico.
    """
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,       # Se elimino il Professional, elimino tutte le sue prenotazioni
        related_name='bookings',        # Permette di fare professional.bookings.all()
    )
    client_name = models.CharField(max_length=100)   # Nome e cognome inseriti dal cliente
    client_email = models.EmailField()               # Email di contatto per conferme/notifiche
    date = models.DateField()                        # Data dell'appuntamento
    time = models.TimeField()                        # Orario dell'appuntamento
    service = models.CharField(max_length=100)       # Servizio scelto (es. "Taglio", "Taglio e barba")
    notes = models.TextField(blank=True)             # Note opzionali del cliente (ritardo, richieste particolari, ecc.)

    def __str__(self):
        # Ritorno una stringa compatta con salone, cliente e data/ora
        return f"{self.professional.business_name} - {self.client_name} - {self.date} {self.time}"
