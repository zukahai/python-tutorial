import tkinter as tk

root = tk.Tk()
root.title("Game kéo búa bao")
label1 = tk.Label(root, text="Lựa chọn của robot", font=("Arial", 16))
label1.pack(pady=10)

label2 = tk.Label(root, text="Lựa chọn của tôi", font=("Arial", 16))
label2.pack(pady=10)

label3 = tk.Label(root, text="Số lần sai", font=("Arial", 16))
label3.pack(pady=10)

root.mainloop()

# Sửa lable1 thành "Lựa chọn của bạn"

label1.config(text="Lựa chọn của bạn")
