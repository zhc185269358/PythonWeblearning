# Python3 实现数据结构



## 二叉树实现:

##### 构造的时候,需要传入每个树节点的数据

```python
class TreeNode():
    def __init__(self,data=None):
        self._data = data
        self._left = None
        self._right = None
        
    def set_data(self,data):
        self._data = data
    
    def get_data(self):
		return self._data
    
    def set_left(self,node):
        self._left = node
        
    def get_left(self):
        return self._left
    
    def set_right(self,node):
        self._right = node
        
    def get_left(self):
        return self._right
    
```

##### 递归实现先\中\后序便利二叉树:

```python
def pre_order(tree):
    if tree == None:
        return False
    print(tree._data)
    pre_order(tree._left)
    pre_order(tree._right)
    
def mid_order(tree):
    if tree == None:
        return False
    mid_order(tree._left)
    print(tree._data)
    mid_order(tree._right)
    
def pos_order(tree):
    if tree == None:
        return False
    pos_order(tree._left)
    pos_order(tree._right)
    print(tree._data)
```

