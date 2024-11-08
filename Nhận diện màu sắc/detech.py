import cv2
import numpy as np
from PIL import Image
import random

# Đọc ảnh từ tệp
image_path = "./assets/images/image.png"
image = cv2.imread(image_path)

image_red = cv2.imread("./assets/images/red.png")
image_blue = cv2.imread("./assets/images/blue.png")
image_yellow = cv2.imread("./assets/images/yellow.png")
image_white = cv2.imread("./assets/images/white.png")

# test = cv2.imread("./assets/tests/0_9.png")

num_rows, num_cols = 10, 10

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

# xem thử test giống với màu nào nhất

def distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

# mã màu red
red_dt = (78, 60, 222)
blue_dt = (215, 176, 77)
yellow_dt = (30, 233, 237)
white_dt = (225, 223, 217)

def distance_color(dt, red):
    score = 0
    for key in red:
        d = distance(key, dt)
        if d < 80:
            score += red[key]
    return score

dts = [red_dt, blue_dt, yellow_dt, white_dt]

# trả về "red", "blue", "yellow", "white"
def get_color(dts, cnt):
    # texts = ["red", "blue", "yellow", "white"]
    texts = [2, 1, 3, 0]
    scores = []
    for dt in dts:
        scores.append(distance_color(dt, cnt))
    # print(scores)
    index = scores.index(max(scores[0:3]))
    if len(dts) > 3 and scores[index] * 7 < scores[3]:
        index = 3
    return texts[index]

# xử lý ảnh

def get_data(data, image):
    # lưu 5 tạo độ có data != 0
    data_ = []
    for i in range(num_rows):
        for j in range(num_cols):
            if data[i][j] != 0:
                data_.append((i, j))
    if len(data_) > 0:
        # random 1 tạo độ
        i, j = data_[random.randint(0, len(data_) - 1)]
    
        # Cắt ảnh i, j
        x = i * image.shape[0] // num_rows
        y = j * image.shape[1] // num_cols
        w = image.shape[0] // num_rows
        h = image.shape[1] // num_cols
        img = image[x:x+w, y:y+h , :]

        c = get_color(dts, cnt_nonzero(img))
        if c != data[i][j]:
            return get_color_image(image)

    # Tìm chỉ số i, j đầu tiên có data = 0
    for i in range(num_rows):
        for j in range(num_cols):
            if data[i][j] == 0:
                x = i * image.shape[0] // num_rows
                y = j * image.shape[1] // num_cols
                w = image.shape[0] // num_rows
                h = image.shape[1] // num_cols
                img = image[x:x+w, y:y+h , :]

                data[i][j] = get_color(dts, cnt_nonzero(img))
                return data
    return data
                

def get_color_image(image):
    is_pop = False
    data = [[0 for _ in range(num_cols)] for _ in range(num_rows)]


    for i in range(num_rows - 1, -1, -1):
        for j in range(num_cols - 1, -1, -1):
            # cắt ảnh
            x = i * image.shape[0] // num_rows
            y = j * image.shape[1] // num_cols
            w = image.shape[0] // num_rows
            h = image.shape[1] // num_cols
            img = image[x:x+w, y:y+h , :]

            data[i][j] = get_color(dts, cnt_nonzero(img))
            if data[i][j] != 0 and is_pop == False and len(dts) > 3:
                # xoá dts cuối
                dts.pop()
                is_pop = True

            # lưu ảnh
            cv2.imwrite(f"./assets/tests/{i}_{j}.png", img)
    dts.append(white_dt)
    return data

if __name__ == "__main__":
    # data = get_color_image(image)
    # for row in data:
    #     print(row)
    image = cv2.imread("./assets/tests/0_0.png")
    cnt = cnt_nonzero(image)
    print(get_color(dts, cnt))







