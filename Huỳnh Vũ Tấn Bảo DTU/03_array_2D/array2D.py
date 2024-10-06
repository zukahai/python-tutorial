s = input().split()
m = int(s[0])
n = int(s[1])

a = []

for i in range(0, m):
    s = input().split() # ['1', '2', '3']
    t = list(map(int, s)) # [1, 2, 3]
    a.append(t)

# for i in range(0, m):
#     for j in range(0, n):
#         print(a[i][j], end=' ')
#     print() # cout << endl;

print(sum(a))

