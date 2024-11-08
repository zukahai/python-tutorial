import pyautogui
import cv2
import numpy as np
from screeninfo import get_monitors
from PIL import Image, ImageDraw, ImageFont
import json

class ScreenCapture:
    def __init__(self, monitor_index=0):
        """
        Khởi tạo class với chỉ số màn hình.
        
        Args:
            monitor_index (int): Chỉ số của màn hình cần chụp.
        """
        self.monitor_index = monitor_index
        self.monitors = get_monitors()
        self.monitor = self.monitors[self.monitor_index]
        
        self.top_left = None
        self.bottom_right = None
        self.camera = self.read_file()
        print("Camera:", self.camera)

    def read_file(self, file_path="./assets/settings.json"):
        """
        Đọc nội dung x, y từ file JSON.
        """
        with open(file_path, "r") as file:
            data = json.load(file)
            self.camera = (data["x"], data["y"])
            return self.camera

    def get_screenshot(self):
        """
        Chụp toàn bộ màn hình và trả về dưới dạng một numpy array.
        """
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
        return screenshot

    def select_region(self):
        """
        Cho phép người dùng chọn vùng cần chụp bằng cách click chuột.
        """
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if self.top_left is None:
                    self.top_left = (x + self.camera[0], y + self.camera[1])
                elif self.bottom_right is None:
                    self.bottom_right = (x + self.camera[0], y + self.camera[1])
                    cv2.destroyAllWindows()
        
        # Hiển thị toàn bộ màn hình và cho phép chọn vùng
        screenshot = self.get_screenshot()
        
        # Chuyển đổi ảnh screenshot sang đối tượng PIL để thêm text
        pil_image = Image.fromarray(screenshot)
        draw = ImageDraw.Draw(pil_image)
        
        # Đường dẫn font (nếu máy bạn có font hỗ trợ tiếng Việt)
        # Bạn có thể thay đổi đường dẫn tới font khác có sẵn trên máy
        font_path = "arial.ttf"  # Hoặc đường dẫn đầy đủ đến file font
        font = ImageFont.truetype(font_path, 60)  # Kích thước font 24
        
        # Thêm dòng chữ
        text = "Vui lòng click chuột vào góc trên trái và góc dưới phải"
        text_position = (10, 10)  # Vị trí hiển thị dòng chữ
        text_color = (255, 0, 0)  # Màu chữ (RGB format)
        
        draw.text(text_position, text, font=font, fill=text_color)
        
        # Chuyển đổi ảnh PIL ngược lại sang numpy array để hiển thị với OpenCV
        screenshot_with_text = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        cv2.imshow("Select Region", screenshot_with_text)
        cv2.setMouseCallback("Select Region", click_event)
        cv2.waitKey(0)

    def capture_region(self):
        """
        Chụp màn hình trong vùng được chọn bởi hai điểm.
        """
        if self.top_left and self.bottom_right:
            x1, y1 = self.top_left
            x2, y2 = self.bottom_right
            width = x2 - x1
            height = y2 - y1
            screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
            return screenshot
        else:
            return None

    def start_capturing(self, save_folder="./assets/images"):
        """
        Bắt đầu chụp màn hình liên tục với khoảng thời gian xác định.
        
        Args:
            interval (int): Khoảng thời gian giữa các lần chụp (giây).
            save_folder (str): Thư mục lưu ảnh chụp.
        """
        import os
        os.makedirs(save_folder, exist_ok=True)
        
        count = 0
        try:
            screenshot = self.capture_region()
            if screenshot:
                file_path = f"{save_folder}/image.png"
                screenshot.save(file_path)
                count += 1
        except KeyboardInterrupt:
            print("Đã dừng chụp màn hình.")

# Sử dụng
if __name__ == "__main__":
    capturer = ScreenCapture()
    capturer.select_region()
    capturer.start_capturing()
