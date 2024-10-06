import speech_recognition
from gtts import gTTS
from playsound import playsound
from datetime import date
import os

end = True

while end:
    robot_ear = speech_recognition.Recognizer()
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
        robot_brain = "Xin chào, tôi là robot."
    elif "hôm nay" in you.lower():
        today = date.today()
        robot_brain = f"Hôm nay là ngày {today.day} tháng {today.month} năm {today.year}."
    elif "tạm biệt" in you:
        end = False
        robot_brain = "Tạm biệt, hẹn gặp lại bạn sau."
    else:
        robot_brain = "Tôi chưa hiểu bạn nói gì."

    tts = gTTS(text=robot_brain, lang='vi')
    tts.save("robot_response.mp3")

    print("Robot: " + robot_brain)
    playsound("robot_response.mp3")
    os.remove("robot_response.mp3")
