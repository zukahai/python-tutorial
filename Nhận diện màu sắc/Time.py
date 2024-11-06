import requests
import base64

def get_gitignore_from_github():
    url = "https://api.github.com/repos/zukahai/python-tutorial/contents/.gitignore"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        
        # GitHub trả về dữ liệu mã hóa base64, vì vậy cần giải mã
        content = response.json().get("content")
        decoded_content = base64.b64decode(content).decode('utf-8')
        
        print("Nội dung của tệp .gitignore:")
        print(decoded_content)
        return decoded_content
        
    except requests.exceptions.RequestException as e:
        print("Không thể lấy dữ liệu từ GitHub:", e)
        return None

# Gọi hàm để lấy nội dung tệp .gitignore
get_gitignore_from_github()
