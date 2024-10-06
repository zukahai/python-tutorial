s = input().split()
m = int(s[0])
n = int(s[1])

a = []

for i in range(0, m):
    s = input().split() # ['1', '2', '3']
    t = list(map(int, s)) # [1, 2, 3]
    a.append(t)


s = 0
for x in a:
    s += sum(x)
print(s)
