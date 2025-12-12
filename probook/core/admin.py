from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Professional, User, Booking


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin personalizzato per il modello User esteso.
    Riutilizza UserAdmin di Django ma:
    - mostra in lista username, email e permessi base
    - ordina gli utenti per ID.
    """
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    ordering = ('id',)


# Registrazione standard dei modelli business
# Professional: ogni salone/studio collegato a un utente
admin.site.register(Professional)

# Booking: tutte le prenotazioni create dai clienti
admin.site.register(Booking)
