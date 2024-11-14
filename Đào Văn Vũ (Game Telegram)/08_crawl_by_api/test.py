import requests
import gdown

def download_file(file_id):
    output = "./08/data/" +file_id + ".pdf"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)
    print(f"Tệp đã được tải về với tên: {output}")

url = "https://pieq.vercel.app/_code/genarator/data.json?_=1731482726550"
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "vi,en-US;q=0.9,en;q=0.8",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"YaBrowser\";v=\"24.10\", \"Yowser\";v=\"2.5\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
}
referrer = "https://pieq.vercel.app/_code/"

# Make the GET request
response = requests.get(url, headers=headers)

# Print the response JSON data
data = []
if response.status_code == 200:
    data = response.json() # Chuyển dữ liệu về dạng JSON
else:
    print(f"Request failed with status code: {response.status_code}")

for row in data:
    t = row['link'].split('?id=')
    print(t[1])
    download_file(t[1])
