ch = input()

if ch.isupper():
    print("Ký tư in hoa")
elif ch.islower():
    print("Ký tự in thường")
elif ch.isdigit():
    print("Ký tự số")
else:
    print("Ký tự đặc biệt")
