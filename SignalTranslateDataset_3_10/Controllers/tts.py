from time import sleep

# pyttsx3: 2.90
import pyttsx3


class Spech:
    def __init__(self, rate=100, volume=1.0, voice=0):
        self.engine = pyttsx3.init('sapi5')

        self.engine.runAndWait()

        self.engine.setProperty('rate', rate)

        self.engine.setProperty('volume', volume)

        voices = self.engine.getProperty('voices')

        self.engine.setProperty('voice', voices[voice].id)

    def Hablar(self, text=""):
        if (len(text) == 0):
            return
        self.engine.say(text)
        self.engine.runAndWait()

    def Oracion(self, oracion):
        self.Hablar(oracion.strip())

    def Parrafo(self, parrafo=""):
        oraciones = parrafo.split(".")
        for oracion in oraciones:
            self.Oracion(oracion)
            sleep(0.5)

    def Histoia(self, historia=""):
        parrafos = historia.split(".\n")
        for parrafo in parrafos:
            self.Parrafo(parrafo)
            sleep(1)

    def Guardar(self, text="", dir="soundOfText.mp3"):
        self.engine.save_to_file(text, dir)
        self.engine.runAndWait()