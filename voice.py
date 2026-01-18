import speech_recognition as sr
import pyttsx3
import threading
from colorama import Fore

class VoiceManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
            self.tts_available = True
        except:
            self.tts_available = False
        
    def listen(self):
        try:
            with sr.Microphone() as source:
                print(Fore.CYAN + "    >> Dinliyorum...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                
            text = self.recognizer.recognize_google(audio, language='tr-TR')
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print(Fore.RED + "    [HATA] Ses tanima servisi kullanilamiyor.")
            return None
        except Exception as e:
            return None
    
    def speak(self, text):
        if not self.tts_available:
            return
            
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
        
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()