from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configurazione dell'app Django principale del progetto (core).
    Qui dichiaro:
    - default_auto_field: tipo di ID predefinito per i modelli (BigAutoField)
    - name: percorso Python dell'app, usato da Django per registrarla.
    L'app core contiene:
    - modello utente esteso
    - modello Professional (salone/studio)
    - modello Booking (prenotazioni)
    e tutte le relative viste/forms/template.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
