# Django--模型学习

- 参考文档 https://yiyibooks.cn/xx/Django_1.11.6/ref/models/options.html

模型是django程序跟数据库交互的ORM,通过模型,我们可以完全以面向对象的方式去思考问题,而不用考虑数据库的SQL语句如何编写

## 基础:

#### 设计思想:

- 每个模型都是一个python类,且,我们定义的 所有模型类都是django.db.models.Model类的子类
- 每个模型类都代表数据库的一张表,而每一个类对象都是该表中的一条记录.
- 每个模型类属性,都是表中的一个字段.字段的数据类型由Field类的子类指定

编写了模型以后,django会为我们提供一套自动生成的API,便于我们执行查询工作.

- 编写模型在生成数据库表时,会用包含这个模型的app名以及model class名来创建 例如polls_Question
- 对于模型来说,最重要的就是列出该模型在数据库中定义的字段.字段由类属性指定

#### 字段类型:

- 模型中每个字段都是相应的Field类的实例

- Django根据Field的类型确定一下信息:

  列类型,告知数据库,要存什么类型的数据

  渲染表单时使用的默认HTMLwidget (例如<input type="text">等)

  最低限度的验证需求,他被用在Django管理站点和自动生成的表单中

#### 字段选项:

- 每个字段都接受一组与字段有关的参数.

- 常用参数介绍:

  - null 设置为True时 django会在数据库中把空值存为NULL.默认为False

  - blank  若为True 该字段允许为空,默认为False

  - 区别:null是纯粹针对数据库,而blank允许表单输入时有一个空值

  - choices:格式是由二元组构成的可迭代对象,用来给该字段提供选项.若设置了该选项,那么,默认的表单被渲染为一个选择框而不是一个标准的文本框

  - ```python
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    )
    在使用时,在Field实例的创建过程中,由choices=这个选项即可
    例如year = models.CharField(max_size=100,choices=YEAR_IN_SCHOOL_CHOICES)
    ```

    默认情况下,primary_key选项是False,如果设置为True,那么该字段就是模型主键,如果不设置,django会为我们自动添加一个

    ```python
    id = models.AutoField(primary_key=True)
    ```

    如果我们在某字段显示指定了primary_key那么它就不再自动添加上述代码了

  - unique : 如果设置为True,那么这个字段在整个表中必须唯一

#### 字段自述名:

###### 	除ForeignKey,ManyToManyField和OneToOne字段,每个字段类型都有一个可选的位置参数,用于提供一个人类易读的字段描述

###### 	ForeignKey,ManyToManyField和OneToOne都要求第一个参数是一个模型类,用于体现关联关系.所以要使用verbose_name关键字参数才能指定自述名

## 模型的关系

###### 	django提供了三种关系ForeignKey,ManyToManyField和OneToOne

#### 多对一关系:

###### 	Django使用ForeignKey定义多对一关系,和使用其它[`Field`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/fields.html#django.db.models.Field)类型一样：在模型当中把它做为一个类属性包含进来

###### 	具体的ForeignKey介绍看这里[`ForeignKey`](https://github.com/zhc185269358/mysite/blob/master/note.md#foreignkey)以及该字段的参数简单介绍

#### 多对多关系:

###### 	ManyToManyField,也需要一个与该模型关联的模型类,表示多对多关系例如，一个`Pizza`可以有多种`Topping` 即一种`Topping` 也可以位于多个Pizza上，而且每个`Pizza`有多个topping

```python
from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
```

- ##### 多对多关系的额外字段

  - 例如，有这样一个应用，它记录音乐家所属的音乐小组。 我们可以用一个[`ManyToManyField`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/fields.html#django.db.models.ManyToManyField) 表示小组和成员之间的多对多关系。
    但是，有时你可能想知道更多成员关系的细节，比如成员是何时加入小组的。
  - 对于这些情况，Django 允许你指定一个中介模型来定义多对多关系。 你可以将其他字段放在中介模型里面。 源模型的[`ManyToManyField`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/fields.html#django.db.models.ManyToManyField) 字段将使用[`through`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/fields.html#django.db.models.ManyToManyField.through) 参数指向中介模型。

  ```python
  from django.db import models
  
  class Person(models.Model):
      name = models.CharField(max_length=128)
  
      def __str__(self):              # __unicode__ on Python 2
          return self.name
  
  class Group(models.Model):
      name = models.CharField(max_length=128)
      members = models.ManyToManyField(Person, through='Membership')
  
      def __str__(self):              # __unicode__ on Python 2
          return self.name
  
  class Membership(models.Model):
      person = models.ForeignKey(Person, on_delete=models.CASCADE)
      group = models.ForeignKey(Group, on_delete=models.CASCADE)
      date_joined = models.DateField()
      invite_reason = models.CharField(max_length=64)
  ```

  在设置中介模型时，要显式地指定外键并关联到多对多关系涉及的模型。 这个显式声明定义两个模型之间是如何关联的。

#### 一对一关系:[`OneToOneField`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/fields.html#django.db.models.OneToOneField)用来定义一对一关系。 和使用其它`Field`类型一样：在模型当中把它做为一个类属性包含进来。



## 跨应用的模型

##### 只需要导入该应用的模型文件中包含的模型类就可以像在本文件内一样使用这个类



## Meta选项

###### 在模型内定义一个class Meta类定义模型的元数据:

```python
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"

```

##### Meta元数据类的其中一个属性:abstract 当设置为True时,这个模型类就不会创建数据表,而是作为基类供其他子类继承以提供信息

##### 模型的元数据:是指任何不是字段的数据 比如:排序选项,数据库表名,具体的Meta完整列表可以参看[Meta模型选项参考](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/options.html).



## 模型属性--objects

###### 	模型最重要的属性是Manger.它是Django模型进行数据库API操作的接口,用于从数据库提取数据,如果没有定义Manager,默认就是objects.Manager 只能通过模型类访问,而不能通过类的实例访问.

## 模型方法

#### 可以在模型上定义自定义的方法来给你的对象添加自定义的“底层”功能。 [`Manager`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/db/managers.html#django.db.models.Manager) 方法用于“表范围”的事务，模型的方法应该着眼于特定的模型实例。

###### 这是一个非常有价值的技术,让业务逻辑位于同一个地方--模型中

- [`__str__()`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/instances.html#django.db.models.Model.__str__)  (python3)

  一个python3的魔法函数,返回对象的unicode格式表示,当模型实例需要强制转换并显示为普通的字符串时，Python 和Django 将使用这个方法。 最明显是在交互式控制台或者管理站点显示一个对象的时候。

- [`get_absolute_url()`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/instances.html#django.db.models.Model.get_absolute_url) 

  - 它告诉Django 如何计算一个对象的URL。 Django 在它的管理站点中使用到这个方法，在其它任何需要计算一个对象的URL 时也将用到。
  - 任何具有唯一标识自己的URL 的对象都应该定义这个方法。



# 模型继承

#### 记住一点,任何编写的自定义类,只要不是要继承另外的自定义类,那么都必须继承[`django.db.models.Model`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/instances.html#django.db.models.Model)类

#### 我们在编写模型时,需要做的决策是想让我们的父类具有自己的数据表,还是只想作为基类提供一些通用方法来减少重用代码

#### Django中有三种风格的继承:

- ##### 通常,我们只想使用父类来持有一些信息,不想在每一个子模型中都敲一遍.这个类永远不会被单独使用,这时我们需要使用`抽象基类 `.

- ##### 如果我们想继承一个已经存在的模型,且想让每个模型具有自己的数据库表,那么应该使用的是多表继承

- ##### 如果想改变一个模块python级别的行为,而不用修改模型字段,使用代理模型



## 抽象基类

#### 编写完基类之后，在 [Meta](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/db/models.html#meta-options)类中设置 `abstract=True` ， 这个模型就不会被用来创建任何数据表。 取而代之的是，当它被用来作为一个其他model的基类时，它的字段将被加入那些子类中。 如果抽象基类和它的子类有相同的字段名，那么将会出现error（并且Django将抛出一个exception）。

```python
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

```

#### `Meta继承`

##### 当一个抽象基类被创建的时候, Django把你在基类内部定义的 [Meta](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/db/models.html#meta-options) 类作为一个属性使其可用。 如果子类没有声明自己的[Meta](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/db/models.html#meta-options)类, 它将会继承父类的[Meta](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/db/models.html#meta-options)。 如果子类想要扩展父类的[Meta](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/db/models.html#meta-options)类，它可以子类化它。

```python
from django.db import models

class CommonInfo(models.Model):
    # ...
    class Meta:
        abstract = True
        ordering = ['name']

class Student(CommonInfo):
    # ...
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'
```



## 多表继承

##### 	这是 Django 支持的第二种继承方式。使用这种继承方式时，每一个层级下的每个 model 都是一个真正意义上完整的 model 。 每个 model 都有专属的数据表，都可以查询和创建数据表。 继承关系在子 model 和它的每个父类之间都添加一个链接 (通过一个自动创建的 [`OneToOneField`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/fields.html#django.db.models.OneToOneField)来实现)。

```python
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

