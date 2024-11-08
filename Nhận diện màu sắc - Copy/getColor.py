import cv2
import numpy as np

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

image_t = cv2.imread("white.png")
t = cnt_nonzero(image_t)

r_avg = 0
g_avg = 0
b_avg = 0
for key in t:
    r, g, b = key
    r_avg += r * t[key]
    g_avg += g * t[key]
    b_avg += b * t[key]
r_avg //= sum(t.values())
g_avg //= sum(t.values())
b_avg //= sum(t.values())

print(r_avg, g_avg, b_avg)