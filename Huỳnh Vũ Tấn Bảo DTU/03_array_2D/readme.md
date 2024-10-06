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


## ord()

Dùng để chuyển một ký tự thành mã ASCII.

```python

a = 'A'
b = ord(a)
print(b) # 65
```

## chr()

Dùng để chuyển một mã ASCII thành ký tự.

```python

a = 65
b = chr(a)
print(b) # 'A'
```

## isLower()

Dùng để kiểm tra một ký tự có phải là chữ thường không.

```python

a = 'a'
b = a.isLower()
print(b) # True
```

## isUpper()

Dùng để kiểm tra một ký tự có phải là chữ hoa không.

```python

a = 'A'
b = a.isUpper()
print(b) # True
```

## isDigit()

Dùng để kiểm tra một ký tự có phải là số không.

```python

a = '1'
b = a.isDigit()
print(b) # True
```
