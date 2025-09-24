import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

class UIService:
    def __init__(self, root):
        self.root = root
        self.root.title("Вторая лаба")
        self.root.geometry("400x300")
        self.audio_path = ""

        self.label = tk.Label(root, text="Вторая лаба", font=("Arial", 14))
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Загрузить аудиофайл (MP3/WAV)", command=self.load_audio)
        self.load_button.pack(pady=5)

        self.trim_button = tk.Button(root, text="Обрезать первые 5 секунд", command=self.trim_audio)
        self.trim_button.pack(pady=5)

        self.normalize_button = tk.Button(root, text="Нормализовать громкость", command=self.normalize_audio)
        self.normalize_button.pack(pady=5)

        self.echo_button = tk.Button(root, text="Добавть Эхо", command=self.add_echo)
        self.echo_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Сохранить аудиофайл", command=self.save_audio)
        self.save_button.pack(pady=5)

        self.status_label = tk.Label(root, text="Не был загружен аудиофайл", wraplength=350)
        self.status_label.pack(pady=10)

    def send_request(self, service_url, data=None):
        try:
            response = requests.post(service_url, json=data) if data else requests.get(service_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Service error: {str(e)}")
            return None

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.audio_path = file_path
            status = self.send_request("http://localhost:5001/process/load", {"file_path": file_path})
            if status:
                self.send_request("http://localhost:5003/history/add", {"file": os.path.basename(file_path), "action": "Загружено"})
                self.status_label.config(text=status["status"])

    def trim_audio(self):
        if self.audio_path:
            status = self.send_request("http://localhost:5001/process/trim", {"file_path": self.audio_path})
            if status:
                self.send_request("http://localhost:5003/history/add", {"file": os.path.basename(self.audio_path), "action": "Обрезано"})
                self.status_label.config(text=status["status"])

    def normalize_audio(self):
        if self.audio_path:
            status = self.send_request("http://localhost:5001/process/normalize", {"file_path": self.audio_path})
            if status:
                self.send_request("http://localhost:5003/history/add", {"file": os.path.basename(self.audio_path), "action": "Нормализовано"})
                self.status_label.config(text=status["status"])

    def add_echo(self):
        if self.audio_path:
            status = self.send_request("http://localhost:5001/process/echo", {"file_path": self.audio_path})
            if status:
                self.send_request("http://localhost:5003/history/add", {"file": os.path.basename(self.audio_path), "action": "Добавлено эхо"})
                self.status_label.config(text=status["status"])

    def save_audio(self):
        if self.audio_path:
            status = self.send_request("http://localhost:5001/process/save", {"file_path": self.audio_path})
            if status:
                self.send_request("http://localhost:5003/history/add", {"file": os.path.basename(status["output_path"]), "action": "Сохранено"})
                messagebox.showinfo("Success", status["status"])

if __name__ == "__main__":
    root = tk.Tk()
    app = UIService(root)
    root.mainloop()