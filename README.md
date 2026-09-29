# Fake Ransomware Enrico Papi

Un'applicazione goliardica scritta in Python con GUI in **Tkinter** che simula una schermata di attacco ransomware a schermo intero, riproduce in background il video da YouTube della famosa pubblicità di Enrico Papi e alla fine di un conto alla rovescia verrà riavviato il PC.

> ⚠️ **DISCLAIMER:** Questo script è creato a puro scopo illustrativo, educativo o di intrattenimento (scherzo innocuo). **NON** cripta né elimina realmente alcun file presente sul computer. Tuttavia, provocherà il **riavvio del sistema** allo scadere del timer.

---

## 🚀 Caratteristiche Principali

* **Interfaccia a Schermo Intero Bloccata:** La finestra copre tutto lo schermo, rimane sempre in primo piano (`topmost`) e disabilita i metodi tradizionali di chiusura (come la `X` o `Alt+F4`).
* **Download Video Automatico:** Scarica un video da YouTube in background senza bloccare la GUI tramite la libreria `yt-dlp`.
* **Riproduzione Video Multipla:** Avvia più finestre del video scaricato (tramite VLC Player o il lettore predefinito di sistema).
* **Conto alla Rovescia:** Mostra un timer configurabile (di default 60 secondi).
* **Riavvio del Sistema:** Allo scadere del timer, termina i processi del video, elimina il file scaricato ed esegue il riavvio automatico del PC.
* **Tasto di Sicurezza Segreto:** Permette all'utente che conosce lo script di chiudere l'applicazione in qualsiasi momento senza riavviare il PC.

---

## 🛠️ Requisiti di Sistema

* **Python 3.x**
* **VLC Media Player** *(consigliato per una corretta riproduzione a loop dei video)*

### Dipendenze Python
L'unica dipendenza esterna richiesta è `yt-dlp`. Le altre librerie usate (`tkinter`, `threading`, `subprocess`, `os`, `sys`, `platform`, `webbrowser`) sono incluse nella libreria standard di Python.

Per installare `yt-dlp`:

```bash
pip install yt-dlp
```

---

## ⚙️ Configurazione

All'inizio del file Python trovi la sezione `--- CONFIGURAZIONE ---` per personalizzare il comportamento dell'applicazione:

```python
YOUTUBE_URL = "https://www.youtube.com/watch?v=jjcCdIkr_TY"  # Link al video YouTube
FILE_VIDEO = "ciao.mp4"                                      # Nome del file MP4 locale salvato
RITARDO_AVVIO_VIDEO_MS = 4000                                # Attesa in ms prima del primo video (4 sec)
DURATA_TIMER_SECONDI = 60                                    # Durata del conto alla rovescia in secondi
NUMERO_FINESTRE_VIDEO = 3                                    # Numero di finestre video che verranno aperte
```

---

## 🎮 Come Utilizzare lo Script

1. Clona o scarica lo script sul tuo computer.
2. Apri un terminale o prompt dei comandi nella cartella del file.
3. Esegui lo script con Python:

```bash
ciao_sono_enrico_papi.py
```

---

## 🔑 Scorciatoia d'Emergenza (Escape Key)

Se desideri interrompere lo scherzo ed uscire dall'applicazione in modo sicuro **senza riavviare il computer**:

* Premere la combinazione di tasti: **`CTRL + Q`**

Questo comando:
1. Chiuderà immediatamente tutte le istanze del video aperti (incluso il processo VLC).
2. Eliminerà il file video temporaneo scaricato sul disco (`ciao.mp4`).
3. Chiuderà la finestra principale dell'applicazione.
