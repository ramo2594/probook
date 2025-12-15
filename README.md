# ProBook – Sistema di prenotazione per saloni e studi

ProBook è una web app sviluppata con Django che permette ai clienti di fissare appuntamenti online e ai professionisti (saloni o studi) di gestire le proprie prenotazioni da una dashboard dedicata. Nasce come progetto finale del corso full‑stack Python/Django (240 ore) e mostra un flusso completo di prenotazione end‑to‑end.

## Funzionalità principali

- Prenotazione online per un salone/studio con form pubblico.
- Dashboard professionista con:
  - riepilogo prenotazioni future, di oggi, prossima prenotazione e totale prenotazioni;
  - tabella delle prenotazioni in arrivo.
- Storico completo delle prenotazioni (passate e future) con dettaglio cliente, servizio e note.
- Email di notifica:
  - al professionista per ogni nuova prenotazione;
  - email di conferma al cliente.
- Gestione utenti:
  - modello utente personalizzato con flag `is_professional`;
  - modello `Professional` collegato 1‑a‑1 all’utente;
  - modello `Booking` per le prenotazioni.

## Stack tecnologico

- **Backend:** Python, Django
- **Database:** SQLite (sviluppo)
- **Auth:** Django Auth + modello `User` esteso
- **Frontend:** Django templates, HTML5, CSS custom (layout tipo SaaS)
- **Email:** `send_mail` con backend console (facile da passare a SMTP reale)

## Architettura interna

- Views leggere: gestiscono solo HTTP (request/response, redirect, scelta template).
- Service layer in `core/services/`:
  - `professional_service.py`: logica della dashboard (query e conteggi: future, oggi, prossima, totale).
  - `history_service.py`: logica dello storico prenotazioni (ordinamento dalla più recente alla più vecchia).
  - `booking_service.py`: creazione prenotazione collegata al Professional + invio email a professionista e cliente.
- Questo separa la logica di business dalla presentazione e rende il codice più testabile e manutenibile.

## Struttura del progetto

Cartella root del progetto (questa repo):

- `.venv/` – ambiente virtuale Python (sviluppo, da non committare).
- `probook/` – codice Django:
  - `probook/` – configurazione principale (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`, `manage.py` è nella root di questa cartella).
  - `core/` – app principale:
    - `models.py` – `User`, `Professional`, `Booking`
    - `views.py` – home, dashboard, storico, form pubblico, conferma
    - `forms.py` – `BookingForm` con validazione data non passata
    - `services/` – service layer per dashboard, storico e booking
    - `admin.py` – registrazione modelli in admin
    - `templates/` – template HTML (dashboard, home, booking, storico, ecc.)
    - `static/core/style.css` – stile globale per dashboard, card e form.
- `Pipfile` / `Pipfile.lock` – definizione dipendenze (se si usa Pipenv).
- `README.md` – questo file.

> Nota: il file `db.sqlite3` è il database di sviluppo. Per GitHub è consigliato aggiungerlo al `.gitignore` e rigenerarlo in locale dopo il clone.

## Installazione e avvio (sviluppo)

Di seguito i passi per avviare il progetto partendo dalla root della repo (`PROBOOK`).

### 1. Clonare la repository

```bash
git clone https://github.com/ramo2594/probook.git
cd probook
```

*(usa il tuo fork se il progetto è stato copiato in un altro account GitHub)*

### 2. Creare e attivare l’ambiente virtuale

Con Python standard:

```bash
python -m venv .venv
```

Su Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

> In alternativa, se si vuole usare Pipenv, basta eseguire `pipenv shell` e saltare i passi sul venv.

### 3. Installare le dipendenze

Se usi `requirements.txt`:

```bash
pip install -r requirements.txt
```

Se usi Pipenv:

```bash
pipenv install
```

*(Scegli una sola delle due modalità a seconda di come è stata configurata la repo.)*

### 4. Applicare le migrazioni

Dalla root del progetto, lancia:

```bash
cd probook
python manage.py migrate
```

Questo crea il database SQLite (`db.sqlite3`) con tutte le tabelle necessarie.

### 5. Creare un superuser

```bash
python manage.py createsuperuser
```

Segui le istruzioni in console per impostare username, email e password.

### 6. Avviare il server di sviluppo

```bash
python manage.py runserver
```

L’app sarà disponibile su:

- `http://127.0.0.1:8000/` – home pubblica (cliente)
- `http://127.0.0.1:8000/admin/` – pannello admin Django

### 7. Configurare un profilo Professional

1. Vai su `http://127.0.0.1:8000/admin/` e accedi con il superuser.
2. Crea (o modifica) un utente e, se necessario, imposta `is_professional=True`.
3. Crea un oggetto `Professional` collegandolo all’utente e compilando:
   - `business_name` (nome del salone/studio),
   - `services` (descrizione servizi offerti).

## Flusso di utilizzo

### Lato cliente

- Visita la home `/` e clicca su **“Prenota da \<nome salone\>”**.
- Compila il form con:
  - nome e cognome,
  - email,
  - servizio,
  - data (solo da oggi in avanti),
  - ora,
  - eventuali note.
- Vede la pagina **“Prenotazione confermata”** con tutti i dettagli dell’appuntamento.

### Lato professionista

- Clicca **“Login professionista”** dalla home ed effettua il login.
- Viene reindirizzato alla propria dashboard `/dashboard/me/`, dove trova:
  - metriche di riepilogo (future, oggi, prossima, totale),
  - tabella “Prenotazioni in arrivo”.
- Può aprire lo **Storico prenotazioni** completo da `/dashboard/history/`:
  - storico di tutte le prenotazioni con data, ora, cliente, servizio e note.
- Può effettuare il **logout** dalla dashboard o dallo storico.

## Possibili estensioni future

- Gestione delle disponibilità orarie e degli slot prenotabili.
- Pagamenti online per confermare la prenotazione (es. Stripe / PayPal).
- Notifiche email/SMS reali tramite SMTP o servizi esterni.
- Supporto multi‑salone / multi‑professionista nella stessa installazione.
- Vista calendario avanzata nella dashboard (giorno/settimana/mese).

