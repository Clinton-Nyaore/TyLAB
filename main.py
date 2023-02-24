from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
import vosk
import pyaudio
import json
import sys
import os
import wave


class Main_UI(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("main.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton.clicked.connect(lambda: MainApp.exit())
        self.pushButton_2.clicked.connect(lambda: self.toggle_window_state())
        self.pushButton_3.clicked.connect(lambda: self.showMinimized())
        self.pushButton_5.clicked.connect(lambda: self.start_conversion())
        self.pushButton_6.clicked.connect(lambda: self.stopConversion())
        self.pushButton_7.clicked.connect(lambda: self.open_file_dialog())
        self.pushButton_8.clicked.connect(lambda: self.convert_file_to_text())

        self.toolButton_4.clicked.connect(lambda: self.help_click())
        self.toolButton_3.clicked.connect(lambda: self.settings_click())

        self.plainTextEdit.setReadOnly(False)
        self.path_to_model = r"./models/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"
        self.model = vosk.Model(self.path_to_model)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

    def start_conversion(self):
        # Start recognizing speech from the microphone
        QMessageBox.information(self, 'Message', 'Session Started, Start recording.', QMessageBox.Ok)
        self.stream.start_stream()
        while True:
            data = self.stream.read(8000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                print("Speak ......... ")
                result = self.recognizer.Result()
                result = json.loads(result)
                my_text = result["text"]
                print("Result:", my_text)
                self.plainTextEdit.setPlainText(self.plainTextEdit.toPlainText() + my_text + " ")
                with open("recorded_text.txt", "a") as f:
                    f.write(my_text + " ")
                QApplication.processEvents()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def open_file_dialog(self):
        # Show the file dialog and allow the user to select an audio file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Audio File', os.path.expanduser('~'), 'Audio Files (*.mp3 *.wav)')

        # Do something with the selected file
        if file_name:
            print(f'Selected file: {file_name}')
            #self.label_3.setText(os.path.basename(file_name))
            self.label_3.setText(file_name)
            self.file_name = file_name
    
    def convert_file_to_text(self):
        # Open the audio file and create the recognizer
        with wave.open(self.file_name, 'rb') as audio_file:
            audio_recognizer = vosk.KaldiRecognizer(self.model, audio_file.getframerate())

            # Loop through the audio data and feed it to the recognizer
            while True:
                data = audio_file.readframes(4000)
                if len(data) == 0:
                    break
                if audio_recognizer.AcceptWaveform(data):
                    result = json.loads(audio_recognizer.Result())
                    text = result["text"]
                    print(text)
                    # Open a new file for writing and write the transcribed text to it
                    with open('transcribed.txt', 'a') as output_file:
                        output_file.write(text + ' ')

    def stopConversion(self):
        # Stop recognizing speech from the microphone
        # Stop the microphone stream
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        # Display a message to inform the user that the speech recognition session has ended
        QMessageBox.information(self, 'Message', 'Session Ended, Your Work was Saved Successfully.', QMessageBox.Ok)

    def help_click(self):
        # Start recognizing speech from the microphone
        QMessageBox.information(self, 'Message', 'Make sure your mic works fine.', QMessageBox.Ok)

    def settings_click(self):
        # Start recognizing speech from the microphone
        QMessageBox.information(self, 'Message', 'Everything seems fine.', QMessageBox.Ok)

    def MoveWindow(self, event):
        if self.isMaximized() == False:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()
            pass
    
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        pass

    def toggle_window_state(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

if __name__ == "__main__":
	MainApp = QApplication(sys.argv)
	App = Main_UI()
	App.show()
	sys.exit(MainApp.exec_())

    