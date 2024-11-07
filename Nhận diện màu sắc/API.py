import requests
import base64

def get_gitignore_from_github():
    try :
        response = requests.get("https://raw.githubusercontent.com/zukahai/python-tutorial/refs/heads/main/.gitignore")
        # lấy dòng thứ nhất
        return response.text.split("\n")[0]

    except requests.exceptions.RequestException as e:
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

if __name__ == "__main__":
    print(get_gitignore_from_github())
