import tkinter as tk
import vosk
import json
import pyaudio

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.model = vosk.Model(r"./models/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.rec = vosk.KaldiRecognizer(self.model, 16000)

        self.title("Offline Voice to Text")

        self.text_area = tk.Text(self, wrap='word')
        self.text_area.grid(row=0, column=1, padx=10, pady=10)

        self.prev_text = ""
        self.recording = False
        self.dark_mode = False

        self.start_button = tk.Button(self, text="Start", command=self.start_recording, bg='#333', fg='#FFF', height=1, width=10, relief=tk.SUNKEN, font=("Helvetica", 16))
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_recording, bg='#333', fg='#FFF', height=1, width=10, relief=tk.SUNKEN, font=("Helvetica", 16))
        self.stop_button.grid(row=1, column=0, padx=10, pady=10)
        self.stop_button.config(state="disabled")

        self.start_button = tk.Button(self, text="Help", command=self.on_help_button_click, bg='#333', fg='#FFF', height=1, width=10, relief=tk.SUNKEN, font=("Helvetica", 16))
        self.start_button.grid(row=2, column=0, padx=10, pady=10)

        self.dark_mode_button = tk.Button(self, text="Dark mode", command=self.toggle_dark_mode, bg='#333', fg='#FFF', height=1, width=10, relief=tk.SUNKEN, font=("Helvetica", 16))
        self.dark_mode_button.grid(row=3, column=0, padx=10, pady=10)

    def start_recording(self):
        self.recording = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.listen()

    def stop_recording(self):
        self.recording = False
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")

    def on_help_button_click(self):
        my_text = """1. Make sure your voice is clear.
        \n2. Ensure your mic is connected and working correctly.
        \n3. NO internet connection is needed."""
        self.text_area.insert("end", my_text)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.config(bg='#333')
            self.text_area.config(bg='#333', fg='#FFF')
        else:
            self.config(bg='#FFF')
            self.text_area.config(bg='#FFF', fg='#000')

    def listen(self):
        if not self.recording:
            return
        data = self.stream.read(8000, exception_on_overflow=False)
        if len(data) == 0:
            print("Error : Check your code !! ")
        if self.rec.AcceptWaveform(data):
            result = self.rec.Result()
            result = json.loads(result)
            recognized_text = result["text"]
            if recognized_text[-1] in ['.', '!', '?']:
                self.prev_text += recognized_text + '\n'
            else:
                self.prev_text += ' ' + recognized_text
            self.text_area.delete("1.0", "end")
            self.text_area.insert("end", self.prev_text)
        self.after(100, self.listen)

if __name__ == "__main__":
    app = App()
    app.mainloop()




