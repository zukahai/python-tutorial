import random
import time

# Initialize the game with a random number
number = random.randint(20, 40)

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

# Start of the game
print(f"Chào mừng đến với trò chơi rút số.\nTôi và bạn sẽ rút lần lượt các số trong số {number}.")
print("Người rút số cuối cùng là người thắng cuộc (Nghĩa là cần rút về số 0).")
print("Lưu ý, số cần rút phải là 1, 2 hoặc 5.")

while True:
    # Get user input
    print(f"Số còn lại: {number}")
    you = input("Con số bạn muốn rút là: ")

    # Validate the user's input
    try:
        x = int(you)
    except ValueError:
        print("Vui lòng nhập một số hợp lệ.")
        continue

    if x > number:
        print(f"Con số bạn chọn lớn hơn {number}, vui lòng chọn lại.")
    elif not isNumberTrue(x):
        print("Con số bạn chọn không hợp lệ, phải là 1, 2 hoặc 5. Vui lòng chọn lại.")
    else:
        number -= x
        print(f"Con số bạn chọn là {x}, số còn lại là {number}.")

        if number == 0:
            print("Chúc mừng bạn đã thắng cuộc!")
            break

        # Robot's turn
        rp = ai(number)
        number -= rp
        time.sleep(0.5)
        print(f"Tôi chọn số {rp}, số còn lại là {number}.")

        if number == 0:
            time.sleep(0.5)
            print("Tôi đã thắng, bạn đã thua.")
            break
