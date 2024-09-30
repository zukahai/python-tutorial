def sum_digit(n):
    sum = 0
    while n > 0:
        sum += (n % 10) ** 2
        n //= 10
    return sum

a = int(input())
list = []
while True:
    a = sum_digit(a)
    if a in list:
        print("NO")
        print(list)
        break
    list.append(a)
    if a == 1:
        print("YES")
        print(list)
        break