# Django--视图



## Django的快捷函数

##### `django.shortcuts` 收集了“跨越” 多层MVC 的辅助函数和类。 换句话讲，这些函数/类为了方便，引入了可控的耦合。

- ### render():

  - ##### `render`(*request*, *template_name*, *context=None*, *content_type=None*, *status=None*, 	*using=None*)[[source\]](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/_modules/django/shortcuts.html#render)

    - ##### 从该函数的语法能看出,第一个位置参数,必须是一个request对象.后续全都是默认参数.

    - ##### 它的功能是: 结合一个给定的模板,带上context上下文,进行渲染,并最终返回一个HttpResponse对象

  - #### 必须参数:

    - #### requeset: 

      - ##### 该request对象,用于生成一个针对该请求的response对象

    - #### template_name:

      - ##### 指定这个视图要渲染并返回的模板名称,或者是一个模板名称的序列,如果给出的是一个序列,那么将使用存在的第一个模板.

  - #### 可选参数:

    - ##### context: 一个字典类型的值.用于将数据传入模板,在此处的字典中的key值必须与模板中要使用该key对应的value的值的变量名称一致.如果字典中的某个值是可调用的,那么会在渲染模板前调用它.

    - ##### conten_type: 用于生成文档的MIME类型. 默认是[`DEFAULT_CONTENT_TYPE`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/settings.html#std:setting-DEFAULT_CONTENT_TYPE)设置的值

    - ##### status: 响应的状态代码。 默认为`200`。

    - ##### using:用于加载模板使用的模板引擎的[`NAME`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/settings.html#std:setting-TEMPLATES-NAME)。

- ### `get_object_or_404()`

  - ##### `get_object_or_404`(*klass*, **args*, **\*kwargs*)[[source\]](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/_modules/django/shortcuts.html#get_object_or_404) 

    - ##### 在一个给定的模型管理器上调用[`get()`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/querysets.html#django.db.models.query.QuerySet.get)，但是引发[`Http404`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/http/views.html#django.http.Http404) 而不是模型的[`DoesNotExist`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/instances.html#django.db.models.Model.DoesNotExist) 异常。

  - ##### 必须参数: 

    - klass
      - 获取该对象的一个[`Model`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/instances.html#django.db.models.Model) 类，[`Manager`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/db/managers.html#django.db.models.Manager)或[`QuerySet`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/models/querysets.html#django.db.models.query.QuerySet) 实例。
    - **kwargs
      - 查询的参数，格式应该可以被`get()` 和`filter()`接受。

    ```python
    from django.shortcuts import get_object_or_404
    
    def my_view(request):
        my_object = get_object_or_404(MyModel, pk=1)
        #get_object_or_404(Book, title__startswith='M', pk=1)
        # 因为第二个参数是收集关键字参数,所以可以包含多个查询条件.
        # 这会直接从模型对应的数据库中直接按条件查询出响应结果
    ```





## 装饰器

#### Django为视图提供了数个装饰器，用以支持相关的HTTP服务。



### 允许的HTTP方法:

##### [`django.views.decorators.http`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/http/decorators.html#module-django.views.decorators.http) 包里的装饰器可以基于请求的方法来限制对视图的访问。 若条件不满足会返回 [`django.http.HttpResponseNotAllowed`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpResponseNotAllowed)。

- ##### `require_http_methods`(*request_method_list*)

  ###### 装饰器要求视图只接受特定的请求方法。 用法：

- ```python
  from django.views.decorators.http import require_http_methods
  
  @require_http_methods(["GET", "POST"])
  def my_view(request):
      # I can assume now that only GET or POST requests make it this far
      # ...
      pass
  ```

  ##### `require_GET`()

  ###### 装饰器要求视图只接受GET方法。

- ##### `require_POST`():

  ###### 装饰器要求视图只接受POST方法。

- ##### `require_safe`():

  装饰器要求视图只接受GET和HEAD方法。

  ###### 这些方法通常被认为是安全的，因为方法不该有请求资源以外的目的。



### 条件视图处理:

##### 	[`django.views.decorators.http`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/http/decorators.html#module-django.views.decorators.http) 中的以下装饰器可以用来控制特定视图的`缓存行为`。

- #####  `condition`（*etag_func=None*，*last_modified_func=None*）[[source\]](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/_modules/django/views/decorators/http.html#condition) 

- #####  `etag`(*etag_func*)[[source\]](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/_modules/django/views/decorators/http.html#etag)

- #####  `last_modified`(*last_modified_func*)[[source\]](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/_modules/django/views/decorators/http.html#last_modified)

  ##### 这些装饰器可用于生成`ETag`和`Last-Modified`标题；见[conditional view processing](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/conditional-view-processing.html)。 



### 缓存:

#### [`django.views.decorators.cache`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/topics/http/decorators.html#module-django.views.decorators.cache)中的装饰器控制服务器和客户端缓存。

- #####  `cache_control`(**\*kwargs*)[[source\]](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/_modules/django/views/decorators/cache.html#cache_control)

  ###### 该装饰器通过向其添加所有关键字参数来修补响应的`Cache-Control`头。 有关转换的详细信息，请参见[`patch_cache_control()`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/utils.html#django.utils.cache.patch_cache_control)。 

- #####  `never_cache`(*view_func*)[[source\]](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/_modules/django/views/decorators/cache.html#never_cache)

  ###### 这个装饰师加了一个 `缓存控制： 最大年龄= 0， 无缓存， 没有存储， 必重新验证` 标题到响应，表示页面不应该被缓存。 







# 内置视图:

#### 参考链接:https://yiyibooks.cn/xx/Django_1.11.6/ref/views.html





# HttpRequest和HttpRespn



## `HttpRequest`对象

### 属性:

- #### `HttpRequest.schem`

  - ##### 一个字符串，表示请求的方案（通常是`http` 或`https`）。

- #### `HttpRequest.body`:

  - ##### 一个字节字符串，表示原始HTTP 请求的正文。 它对于处理非HTML 形式的数据非常有用：二进制图像、XML等。 如果要处理常规的表单数据，应该使用[`HttpRequest.POST`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpRequest.POST)。

  - ##### 你还可以使用类似文件的接口从`HttpRequest`中读取数据。 参见[`HttpRequest.read()`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpRequest.read)。

- #### `HttpRequest.path`:

  - ##### 表示请求页面的完整路径的字符串，不包括方案或域。

- #### `HttpRequest.path_info`:

  - ###### 在某些Web 服务器配置下，主机名后的URL 部分被分成脚本前缀部分和路径信息部分。 `path_info` 属性将始终包含路径信息部分，不论使用的Web 服务器是什么。 使用它代替[`path`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpRequest.path) 可以让代码在测试和开发环境中更容易地切换。

- #### `HttpRequest.method`:

  - ###### 一个字符串，表示请求使用的HTTP 方法。 必须使用大写。 

  - ```python
    if request.method == 'GET':
        do_something()
    elif request.method == 'POST':
        do_something_else()
        
    ```

- #### `HttpRequest.encoding`:

  - ###### 一个字符串，表示提交的数据的编码方式（如果为`None` 则表示使用[`DEFAULT_CHARSET`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/settings.html#std:setting-DEFAULT_CHARSET) 设置）。 这个属性是可写的，你可以修改它来修改访问表单数据使用的编码。 任何随后的属性访问（例如从[`GET`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpRequest.GET)或[`POST`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpRequest.POST)读取）将使用新的`encoding`值

- #### `HttpRequest.POST`:

  - ###### 一个包含所有给定的HTTP POST参数的类字典对象，提供了包含表单数据的请求。 详情请参考下面的[`QueryDict`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.QueryDict) 文档。 如果需要访问请求中的原始或非表单数据，可以使用[`HttpRequest.body`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpRequest.body) 属性。

  - ###### POST请求可能带有一个空的`POST`字典 — 如果通过HTTP POST方法请求一个表单但是没有包含表单数据。 所以，你不应该使用`if request.POST`来检查使用的是否是POST方法；请使用`if request.method == "POST"`（参见[`HttpRequest.method`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/request-response.html#django.http.HttpRequest.method)）

- #### `HttpRequest.COOKIES`:

  - ###### 包含所有Cookie的字典。 键和值都为字符串。

- #### `HttpRequest.FILES`:

  - ###### 一个类似于字典的对象，包含所有上传的文件。 `FILES`中的每个键为`<input type="file" name="" />`中的`name`。 `FILES`中的每个值是一个[`UploadedFile`](https://yiyibooks.cn/__trs__/xx/Django_1.11.6/ref/files/uploads.html#django.core.files.uploadedfile.UploadedFile)。

  - ###### 如果请求方法是POST且请求的`<form>`带有`enctype="multipart/form-data"`，那么`FILES`将只包含数据。否则，`FILES`将为一个空的类似于字典的对象。

​	