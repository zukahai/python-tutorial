from datetime import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import os
from playsound import playsound

BabyBoo =pyttsx3.init()
voice = BabyBoo.getProperty('voices')
BabyBoo.setProperty('voice',voice[1].id)

def speak(audio):
    print("BabyBoo: " + audio)
    BabyBoo.say(audio)
    BabyBoo.runAndWait()
def time():
    Time = datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)
def welcome():
    hour = datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning Sir !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")
    elif hour >= 18 and hour < 24:
        speak("Good Evening Sir !")
    else:
        speak("Good Night Sir !")
    speak("How may I help you Sir ?")

def command():
    c=sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 2 #lenh du`ng truoc khi nghe giong noi
        audio = c.listen(source)
        try:
            query = c.recognize_google(audio, language='vi-VN')
            print("Sir: " + query)
        except sr.UnknownValueError:
            return "Please repeat or typing the command"
            query = str(input("Command:Your order is: "))
        return query

if __name__ == "__main__":
    welcome()
    while True:
        query = command().lower()
        if "google" in query:
            speak("What should I search boss?")
            searcj = command().lower()
            url=f'https://www.google.com/search?q={searcj}'
            wb.get().open(url)
            speak(f'Here is your{searcj}on google')
        elif "youtube" in query:
            speak("What should I search boss?")
            searcj = command().lower()
            url=f'https://www.youtube.com/search?q={searcj}'
            wb.get().open(url)
            speak(f'Here is your{searcj}on youtube')
        elif "open video" in query:
            meme=r"C:\Users\DELL\Videos"
            os.startfile(meme)
        elif "time" in query:
            time()
        elif "quit" in query:
            speak("Good Bye Sir")
            exit()