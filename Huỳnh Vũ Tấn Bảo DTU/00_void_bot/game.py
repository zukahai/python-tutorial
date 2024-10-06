import speech_recognition
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import os
import time
import random

number = random.randint(20, 40)

def speak(robot_brain):
    print("Robot: " + robot_brain)
    # name_mp3 = "05-10-2024-23-59-59.mp3"
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

def isNumberTrue(n):
    return n in [1, 2, 5]

def ai(n):
    dp = [0] * (n + 1)
    dp[0] = False
    res = []
    l = [1, 2, 5]
    for i in range(1, n + 1):
        dp[i] = False
        for x in l:
            if i - x >= 0 and dp[i - x] == False:
                dp[i] = True
                break
    for x in l:
        if n - x >= 0 and dp[n - x] == False:
            res.append(x)
    if len(res) == 0:
        return random.randint(1, n)
    return random.choice(res)
            
                
end = True
name_user = ""

robot_ear = speech_recognition.Recognizer()
speak("Chào mừng đến với trò chơi rút số.\nTôi và bạn sẽ rút lần lượt các số trong số {0}.\nNgười rút số cuối cùng là người thắng cuộc (Nghĩa là cần rút về số 0).\nLưu ý, số cần rút phải là 1, 2 hoặc 5".format(number))
while end:
    robot_brain = ""

    with speech_recognition.Microphone() as mic:
        print("Robot: Con số bạn muốn rút là:")
        audio = robot_ear.listen(mic)

    try:
        you = robot_ear.recognize_google(audio, language="vi-VN")
    except speech_recognition.UnknownValueError:
        you = ""

    print("You: " + you)

    if you == "":
        robot_brain = "Tôi không hiểu bạn nói gì, thử lại nhé."
    elif "tạm biệt" in you.lower():
        end = False
        robot_brain = "Tạm biệt {0}, hẹn gặp lại bạn sau.".format(name_user)
    else:
        # Tách số từ câu nói
        numbers = [int(s) for s in you.split() if s.isdigit()]
        if len(numbers) > 0:
            x = numbers[0]
            if x > number:
                robot_brain = "Con số bạn chọn lớn hơn {}, vui lòng chọn lại".format(number)
            elif not isNumberTrue(x):
                robot_brain = "Con số bạn chọn không hợp lệ, phải là 1, 2 hoặc 5, vui lòng chọn lại"
            else:
                number -= x
                robot_brain = "Con số bạn chọn là {}, con số còn lại là {}".format(x, number)
                speak(robot_brain)

                if number == 0:
                    robot_brain = "Chúc mừng bạn đã thắng cuộc"
                    speak(robot_brain)
                    break
                rp = ai(number)
                number -= rp
                time.sleep(0.5)
                robot_brain = "Tôi chọn số {}, số còn lại là {}".format(rp, number)
                if number == 0:
                    speak(robot_brain)
                    time.sleep(0.5)
                    robot_brain = "Tôi đã thắng, bạn đã thua"
                    speak(robot_brain)
                    break
        else:
            robot_brain = "Không tìm thấy con số trong câu nói của bạn."


    speak(robot_brain)
    
