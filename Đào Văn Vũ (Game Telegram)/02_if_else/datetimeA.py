import speech_recognition
import pyttsx3
from datetime import date
from datetime import datetime

robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()
robot_brain = ""

with speech_recognition.Microphone() as mic :
    print("Robot:I'm Listening")
    audio = robot_ear.listen(mic)

print("Robot: ...")
try:
    you = robot_ear.recognize_google(audio)
except:
    you = ""

print("You: " + you)

if you == "":
    robot_brain = "Đéo hiểu mày nói gì, thử lại đi"
elif you.upper() == "Hello".upper():
    robot_brain = "Hello Vũ đẹp trai"
elif you.upper() == "today".upper():

    today = date.today()

    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")
    print("Hôm nay là ngày {0} tháng {1} năm {2}".format(day, month, year))
elif you.upper() == "time".upper:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") 
else:
    robot_brain = "Tiếng việt nói đéo sõi ngu thế"

print("Robot: " + robot_brain)
robot_mouth.say(robot_brain)
robot_mouth.runAndWait()