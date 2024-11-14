import requests
from bs4 import BeautifulSoup

# URL của trang web bạn muốn cào dữ liệu
url = 'https://vn.investing.com/economic-calendar/'

# Gửi yêu cầu HTTP để lấy nội dung của trang
response = requests.get(url)
response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không

# Phân tích cú pháp HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm tất cả các thẻ có class là "flagCur"
items = soup.find_all(class_='js-event-item')

# In ra nội dung của các thẻ đã tìm được
for item in items:
    # print(item.text)  # Hoặc bạn có thể dùng flag.get_text(strip=True) để loại bỏ khoảng trắng

    flag = item.find(class_='flagCur')

    if flag.text[2:] == 'USD':
        print(flag.text[2:])
        time = item.find(class_='time')
        print("TIME", time.text)

        event = item.find(class_='event')
        print(event.text)

        act = item.find(class_='act')
        print("ACT", act.text)

        prev = item.find(class_='prev')
        print("PREV", prev.text)

        fore = item.find(class_='fore')
        print("FORE", fore.text)
        print('----------------------------------------------')
