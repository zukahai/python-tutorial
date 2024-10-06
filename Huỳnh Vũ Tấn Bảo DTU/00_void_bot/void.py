import speech_recognition
from gtts import gTTS
from playsound import playsound
from datetime import date
import os

end = True
name_user = ""

robot_ear = speech_recognition.Recognizer()
while end:
    robot_brain = ""

    with speech_recognition.Microphone() as mic:
        print("Robot: Tôi đang lắng nghe...")
        audio = robot_ear.listen(mic)

    try:
        you = robot_ear.recognize_google(audio, language="vi-VN")
    except speech_recognition.UnknownValueError:
        you = ""

    print("You: " + you)

    if you == "":
        robot_brain = "Tôi không hiểu bạn nói gì, thử lại nhé."
    elif "xin chào" in you.lower():
        robot_brain = "Xin chào, tôi là robot.\n" + "Bạn tên là gì?"
    elif "hôm nay" in you.lower():
        today = date.today()
        robot_brain = "Hôm nay là ngày {0} tháng {1} năm {2}.".format(today.day, today.month, today.year)
    elif "tạm biệt" in you.lower():
        end = False
        robot_brain = "Tạm biệt {0}, hẹn gặp lại bạn sau.".format(name_user)
    elif "tên là " in you.lower():
        robot_brain = "Xin chào " + you.split("tên là ")[1]
        name_user = you.split("tên là ")[1]
    else:
        robot_brain = "Xin lỗi, tôi chưa hiểu bạn nói gì."

    print("Robot: " + robot_brain)
    name_mp3 = date.today().strftime("%Y-%m-%d-%H-%M-%S") + ".mp3"
    try :
        tts = gTTS(text=robot_brain, lang='vi')
        tts.save(name_mp3)
        playsound( name_mp3)
    except:
        print("Error: Cannot play sound")
        pass
    if os.path.exists(name_mp3):
        os.remove(name_mp3)
