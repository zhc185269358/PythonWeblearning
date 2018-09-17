## python 内置函数学习

#### enumerate()函数

enumerate()函数,用于将一个`可遍历的`数据对象(列表,元组或字符串)组合为一个索引序列,同时,列出数据和数据下标,这也就解释了为什么要用两个变量一起去遍历.

enumerate(sequence,[start=0])函数有两个参数:

- sequence 一个序列,迭代器或者刻碟带对象
- start 下标的起始位置

##### 返回值

- 枚举类型对象

##### 举例:

```python
>>>seasons = ['Spring','summer','Fall','Winter']
>>>list(enumerate(seasons))
它返回的就是一个元组,其中元祖的第一个元素就是原来列表中元素的索引,第二个元素是列表值.
可以通过指定start=一个数字,来表示生成的元组中的第一个元素从几开始
```

#### locals()函数

##### 描述:

- 函数会以字典类型返回当前位置的所有局部变量

- 对于函数,方法,lambda函数,类,以及实现了`__call__` 方法的类实例,它都返回True

- ```python
  def runoob(arg):    # 两个局部变量：arg、z
  ...     z = 1
  ...     print (locals())
  {'z':1, 'arg':4}
  ```

#### bin()函数:

##### 描述: 返回一个数字的二进制的字符串表示.