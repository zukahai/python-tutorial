n = (int)(input())
s = input() # Nhập dòng thứ 2
s = s.split() # ['1', '2', '3']

# Ép kiểu về dạng số và thêm và a
a = []
for x in s:
    a.append((int)(x))

for x in a:
    print(x, end=" ")
