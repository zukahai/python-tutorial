import cv2
import numpy as np
from PIL import Image

# Đọc ảnh từ tệp
image_path = "./assets/images/image.png"
image = cv2.imread(image_path)

image_red = cv2.imread("./assets/images/red.png")
image_blue = cv2.imread("./assets/images/blue.png")
image_yellow = cv2.imread("./assets/images/yellow.png")
image_white = cv2.imread("./assets/images/white.png")

test = cv2.imread("./assets/images/test3.png")

num_rows, num_cols = 7, 10

def cnt_nonzero(image):
    # đọc từng pixel của ảnh và đếm tần số xuất hiện của mỗi màu
    width, height, _ = image.shape
    cnt = {}
    for i in range(width):
        for j in range(height):
            pixel = tuple(image[i][j])
            if pixel in cnt:
                cnt[pixel] += 1
            else:
                cnt[pixel] = 1
    cnt = dict(sorted(cnt.items(), key=lambda item: item[1], reverse=True))
    return cnt

red = cnt_nonzero(image_red)
blue = cnt_nonzero(image_blue)
yellow = cnt_nonzero(image_yellow)
white = cnt_nonzero(image_white)

test = cnt_nonzero(test)

# xem thử test giống với màu nào nhất

def distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

# mã màu red
red_dt = (30, 25, 236)
blue_dt = (245, 30, 30)
yellow_dt = (39, 221, 217)
white_dt = (222, 219, 213)

def distance_color(dt, red):
    score = 0
    for key in red:
        if distance(key, dt) < 50:
            score += red[key]
    return score

dts = [red_dt, blue_dt, yellow_dt, white_dt]

# trả về "red", "blue", "yellow", "white"
def get_color(dts, red):
    # texts = ["blue", "red", "yellow", "white"]
    texts = [2, 1, 3, 0]
    scores = []
    for dt in dts:
        scores.append(distance_color(dt, red))
    return texts[scores.index(max(scores))]

# xử lý ảnh

def get_color_image(image):
    data = [[0 for _ in range(num_cols)] for _ in range(num_rows)]


    for i in range(num_rows):
        for j in range(num_cols):
            # cắt ảnh
            x = i * image.shape[0] // num_rows
            y = j * image.shape[1] // num_cols
            w = image.shape[0] // num_rows
            h = image.shape[1] // num_cols
            img = image[x:x+w, y:y+h , :]

            data[i][j] = get_color(dts, cnt_nonzero(img))
    while (len(data) < num_cols):
        data.append([0 for _ in range(num_cols)])

    return data

if __name__ == "__main__":
    data = get_color_image(image)
    print(data)






