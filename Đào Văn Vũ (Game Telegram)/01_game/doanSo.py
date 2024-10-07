import speech_recognition
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import os

def speak(robot_brain):
    print("Robot: " + robot_brain)
    try:
        name_mp3 = datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".mp3"
        tts = gTTS(text=robot_brain, lang='vi')
        tts.save(name_mp3)
        playsound( name_mp3)
    except:
        print("Error: Cannot play sound")
        pass
    if os.path.exists(name_mp3):
        os.remove(name_mp3)

def ear_micro():
    with speech_recognition.Microphone() as mic:
        print("Robot: Tôi đang nghe bạn nói")
        robot_ear.adjust_for_ambient_noise(mic)
        audio = robot_ear.listen(mic, phrase_time_limit=3)
    try:
        you = robot_ear.recognize_google(audio, language="vi-VN")
    except speech_recognition.UnknownValueError:
        you = ""
    return you

robot_ear = speech_recognition.Recognizer()
speak("Chào mừng đến với trò chơi đoán số.\nHãy nghĩ trong đầu một số từ 1 đến 1000, Tôi sẽ đoán số bạn đang nghĩ\nMỗi lượt hãy cho tôi biết số mà tôi đoán đã chính xác, nhỏ hơn hay lớn hơn số bạn nghĩ.\nTôi chỉ cần tối đa 10 lượt đoán để tìm ra số bạn nghĩ.")
speak("Hãy nói: Bắt đầu để bắt đầu trò chơi.")

while True:
    robot_brain = ""
    you = ear_micro()
    if "bắt đầu" in you.lower():
        break
    robot_brain = "Tôi không hiểu bạn nói gì, hãy nói bắt đầu để bắt đầu trò chơi"

speak("Tôi đã bắt đầu trò chơi")

l, r = 1, 1000
count = 0

while l <= r:
    mid = (l + r) // 2
    count += 1
    robot_brain = "Lần {0}: Số bạn nghĩ là {1} phải không?".format(count, mid)
    speak(robot_brain)

    you = ear_micro()
    print("You: {0}".format(you))

    if "chính xác" in you.lower():
        robot_brain = "Tôi đã chiến thắng"
        speak(robot_brain)
        break
    elif "nhỏ" in you.lower():
        r = mid - 1
    elif "lớn" in you.lower():
        l = mid + 1
    else:
        robot_brain = "Tôi không hiểu bạn nói gì, hãy nói chính xác, nhỏ hơn hoặc lớn hơn"
        speak(robot_brain)
        count -= 1
        continue

    if count == 10:
        robot_brain = "Tôi đã hết lượt đoán, bạn đã thắng"
        speak(robot_brain)
        break

speak("Cảm ơn bạn đã chơi trò chơi với tôi")