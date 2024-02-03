import speech_recognition as sr
import pyttsx4, random, pygame, time
from gpt4all import GPT4All


# 定义语音机器人函数
class Jarvis():
    def __init__(self, audiofile_path) -> None:
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.sample_rate = 44100
        self.engine = pyttsx4.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty('voice', self.voices[1].id)
        self.engine.setProperty("rate", 160)
        self.model = GPT4All(r"C:\Users\whuli\AppData\Local\nomic.ai\GPT4All\mistral-7b-instruct-v0.1.Q4_0.gguf", allow_download=False, device='nvidia')
        pygame.init()
        self.user_voice = ''
        self.response = ''
        self.speak_content = ''
        self.audiofile_path = audiofile_path

    def listen_voice(self):
        with sr.Microphone() as source:
            print("Listening........")
            audio = self.recognizer.listen(source, timeout=2)
            self.user_voice = self.recognizer.recognize_google(audio, language='en-US')
            print("You:", self.user_voice)

        return self.user_voice
    
    def model_response(self):
        with self.model.chat_session():
            self.response = self.model.generate(prompt=self.listen_voice(), temp=0, max_tokens=4096)
            print("Jarvis:", self.response)
        return self.response

    def speak_module(self):
        self.engine.say(self.speak_content)
        self.engine.runAndWait()
        self.engine.stop
        

    def reply_jarvis(self):
        self.speak_content = self.model_response()
        self.speak_module()

    def load_audio_file(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.audiofile_path)
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
        
        pygame.quit()


startup_audiofile_path = r'C:\Users\whuli\Desktop\Jarvis\JARVIS-STARTUP-SOUND.wav'
my_jarvis = Jarvis(audiofile_path=startup_audiofile_path)
my_jarvis.load_audio_file()

# 与用户进行语音互动
while True:
    try:
        my_jarvis.reply_jarvis()
        time.sleep(2)
    except Exception as e:
        print(e)
        
