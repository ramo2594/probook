from datetime import date
from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form pubblico usato nella pagina di prenotazione.
    Si appoggia al modello Booking e aggiunge una validazione extra
    per evitare che l'utente scelga una data nel passato.
    """
    class Meta:
        # Modello di riferimento per il form
        model = Booking
        # Campi che esponiamo al cliente nel form pubblico
        fields = ['client_name', 'client_email', 'service', 'date', 'time', 'notes']
        # Widget HTML5 per avere datepicker, timepicker e textarea compatta
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        """
        Validazione personalizzata sul campo 'date'.
        Se la data inserita è precedente a oggi, blocca il form con un messaggio di errore.
        Così il sistema accetta solo prenotazioni da oggi in avanti.
        """
        d = self.cleaned_data['date']
        if d < date.today():
            raise forms.ValidationError(
                "Non puoi prenotare in una data passata. Scegli una data da oggi in poi."
            )
        return d
