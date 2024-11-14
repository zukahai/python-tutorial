import requests
from bs4 import BeautifulSoup

# URL của trang web bạn muốn cào dữ liệu
url = 'https://vn.investing.com/economic-calendar/'

# Gửi yêu cầu HTTP để lấy nội dung của trang
response = requests.get(url)
response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không

# Phân tích cú pháp HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm tất cả các thẻ có class là "js-event-item"
items = soup.find_all(class_='js-event-item')

# Tạo danh sách lưu các bản ghi cào được
messages = []

# Lặp qua từng item và lấy thông tin cần thiết
for item in items:
    flag = item.find(class_='flagCur')
    
    # Kiểm tra nếu tồn tại thẻ flag và lọc theo 'USD'
    if flag and flag.text[2:] == 'USD':
        time = item.find(class_='time')
        event = item.find(class_='event')
        act = item.find(class_='act')
        prev = item.find(class_='prev')
        fore = item.find(class_='fore')
        
        # Tạo nội dung tin nhắn
        message = f"Currency: {flag.text[2:]}\n"
        message += f"Time: {time.text if time else ''}\n"
        message += f"Event: {event.text if event else ''}\n"
        message += f"Actual: {act.text if act else ''}\n"
        message += f"Previous: {prev.text if prev else ''}\n"
        message += f"Forecast: {fore.text if fore else ''}\n"
        message += '-' * 40
        
        # Thêm tin nhắn vào danh sách
        messages.append(message)

# Ghép các bản tin lại thành một tin nhắn lớn
final_message = "\n\n".join(messages)

# Thông tin Telegram Bot
token = 'YOUR_TELEGRAM_BOT_TOKEN'  # Thay YOUR_TELEGRAM_BOT_TOKEN bằng mã token của bạn
chat_id = 'YOUR_CHAT_ID'  # Thay YOUR_CHAT_ID bằng ID của người dùng hoặc nhóm bạn muốn gửi đến

# Gửi tin nhắn đến Telegram
telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'
data = {
    'chat_id': chat_id,
    'text': final_message
}
response = requests.post(telegram_url, data=data)

# Kiểm tra kết quả gửi tin nhắn
if response.status_code == 200:
    print("Tin nhắn đã được gửi thành công!")
else:
    print("Lỗi khi gửi tin nhắn:", response.text)
