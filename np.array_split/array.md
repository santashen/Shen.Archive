### np.array_split

`np.array_split`函数可以实现数组的均匀或者不均匀分割

```python
np.array_split(range(1,5),2)
```

```python
result:[array([1, 2]), array([3, 4])]
```

```python
np.array_split(range(1,6),2)
```

```python
result:[array([1, 2, 3]), array([3, 4])]
```

这个东西在并行化的时候可以用，

```python
from concurrent import futures

def function(interval):
    for i in interval:
       # do something
    
if __name__ == "__main__":
    with futures.ProcessPoolExecutor(8) as executor:
        datasets = list(executor.map(function, np.array_split(range(1, FILE_NUMBER), 8)))
```

同时对大量的数据进行处理，数据之间是独立的，把原先依序执行的for循环体重构为以处理区间为参数的函数，

