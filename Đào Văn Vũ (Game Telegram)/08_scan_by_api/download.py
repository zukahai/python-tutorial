import gdown

def download_file(file_id):
    output = "./08/data/" +file_id + ".pdf"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)
    print(f"Tệp đã được tải về với tên: {output}")

if __name__ == "__main__":
    # ID tệp từ liên kết Google Drive của bạn
    file_id = "14Z_JHETRXcrlEzC3iknwINXmIgGwb9ia"  # Dùng file_id của bạn

    # Gọi hàm để tải tệp
    download_file(file_id)
