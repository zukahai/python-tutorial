import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL của trang web bạn muốn cào dữ liệu
url = 'https://vn.investing.com/economic-calendar/'

# Gửi yêu cầu HTTP để lấy nội dung của trang
response = requests.get(url)
response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không

# Phân tích cú pháp HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm tất cả các thẻ có class là "js-event-item"
items = soup.find_all(class_='js-event-item')

# Tạo danh sách để lưu trữ dữ liệu
data = []

# Lặp qua từng item và lấy thông tin cần thiết
for item in items:
    flag = item.find(class_='flagCur')
    
    # Kiểm tra nếu tồn tại thẻ flag và lọc theo 'USD'
    if flag and flag.text[2:] == 'USD':
        time = item.find(class_='time')
        event = item.find(class_='event')

        # Xoá khoảng trắng ở đầu và cuối chuỗi
        event = event.text.strip()

        act = item.find(class_='act')
        prev = item.find(class_='prev')
        fore = item.find(class_='fore')
        
        # Lưu dữ liệu vào danh sách dưới dạng từ điển
        data.append({
            'Currency': flag.text[2:],         # Lấy mã tiền tệ (ví dụ: USD)
            'Time': time.text if time else '',  # Thời gian
            'Event': event if event else '',  # Sự kiện
            'Actual': act.text if act else '',  # Giá trị thực tế
            'Previous': prev.text if prev else '',  # Giá trị trước đó
            'Forecast': fore.text if fore else ''  # Dự đoán
        })

# Tạo DataFrame từ danh sách dữ liệu
df = pd.DataFrame(data)

# Lưu DataFrame vào file Excel
df.to_excel('economic_calendar_data.xlsx', index=False)

print("Dữ liệu đã được lưu vào file 'economic_calendar_data.xlsx'")
