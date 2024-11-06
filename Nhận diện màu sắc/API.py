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
        
        # dòng đầu tiên của tệp .gitignore
        first_line = decoded_content.split("\n")[0]
        return first_line
        
    except requests.exceptions.RequestException as e:
        print("Không thể lấy dữ liệu từ GitHub:", e)
        return None


def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
    
def API_check():
    data_api = get_gitignore_from_github()
    data_local = read_file("./assets/APIKEY.txt")
    return data_api == data_local


