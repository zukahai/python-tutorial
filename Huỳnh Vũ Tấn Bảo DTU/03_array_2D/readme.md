## a.sort()

Dùng để sắp xếp mảng a theo thứ tự tăng dần.

```python
a = [1, 3, 2, 4, 5]
a.sort()
print(a) # [1, 2, 3, 4, 5]
```

## set()

Dùng để chuyển một mảng thành một tập hợp, loại bỏ các phần tử trùng lặp.

```python

a = [1, 2, 3, 2, 1]
b = set(a)
print(b) # {1, 2, 3}

c = list(b)
print(c) # [1, 2, 3]
```

## map()

Dùng để ánh xạ một hàm lên mỗi phần tử của mảng.

```python

a = ['1', '2', '3']
b = list(map(int, a))
print(b) # [1, 2, 3]
```



