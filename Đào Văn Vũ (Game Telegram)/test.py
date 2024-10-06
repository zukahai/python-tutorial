from datetime import date

# today = date.today()

# day = today.strftime("%d")
# month = today.strftime("%m")
# year = today.strftime("%Y")
# print("Hôm nay là ngày {0} tháng {1} năm {2}".format(day, month, year))

import requests

# Gửi yêu cầu đến World Time API để lấy thời gian UTC
response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    data = response.json()
    
    # Lấy thông tin ngày giờ từ JSON response
    datetime_str = data['datetime']  # Dữ liệu datetime ở định dạng ISO 8601
    
    # Chỉ lấy ngày và giờ từ chuỗi datetime
    date_part = datetime_str.split("T")[0]
    time_part = datetime_str.split("T")[1].split(".")[0]
    
    print("Giờ chuẩn UTC hiện tại là: {0} {1}".format(date_part, time_part))
else:
    print("Không thể lấy dữ liệu thời gian từ API.")
