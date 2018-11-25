# flask框架使用



​	在之前的项目中, 由于需求的改进,需要给单纯的脚本程序添加一个web管理界面,来触发一个手动的程序执行.于是,对程序进行了一个重构,由于页面和项目本身不大,所以考虑使用flask框架来进行项目重构.原本的脚本程序,也重新抽象为一个工具类,方便web框架在接口调用时触发功能.本项目采用了前后端分离的方式,所以并未使用Flask本身的模板引擎,这里不对Jinja2模板引擎做介绍了.



## flask框架的基本使用:

##### 	flask框架是一个给予werkzeug和Jinja2的一个微型web框架,其核心非常简单,同时,框架也由非常多的外部模块的支持,用于项目需求的扩展.flask可以相对自由的选择模板和ORM.



### 开发环境:

​	使用Anaconda3 + pycharm + python3



为了保证开发环境的整洁,我们使用了一个python包管理器anaconda,来为我们的项目创建一个虚拟环境.

```
conca create --name 虚拟环境名(flask_pro)
```

就可以创建一个python虚拟环境了.然后可以开始激活虚拟环境

##### Linux 下激活虚拟环境的命令

```shell
source activate flask_pro
```

##### Win下的是

```shell
activate flask_pro
```

一般在pycharm中进行开发,我们都会通过pycharm来进行包和外部模块的安装.百度即可,不在赘述.

安装flask 和flask-login模块(后续再详述其作用与使用过程)



### Flask框架的具体使用过程:

​	打开pycharm:创建一个普通python项目也可以,一个Flask项目也可以,我自己项目由于是前后端分离,前段的页面都是打包以后,放在项目文件下,页面的编译都放在了服务器上去执行,在项目下只是有一个打包后的文件来作为测试使用,所以这里就使用一个普通的python项目即可.

​	因为flask框架会自动去寻找项目文件下的templates目录下的页面以及静态资源,所以,前段同事在做页面的整合打包时,都是按照Flask框架的基本项目结构来的,这里简单介绍一下一个flask项目的目录结构.

​	我个人觉得学习一个web框架,想要快速上手,快速建立起一个最简单的项目是比较重要的,至于说原理,可以在使用过程中进行研究,加深理解.了解项目结构,有助于我们理解每一个文件的具体含义,和大致的开发流程.帮助我们快速做好开发前的准备工作.包括一些数据库,和其他东西的配置.

Flask框架的基本目录结构如下:

一个基本的app.py文件,同级的一个templates包和一个static包,分别是用来放网页和静态资源(css文件和js文件,图片或者其他文件),

```
-----app
-----templates(是一个包)
-----static(是一个包)
```

​	到后续,如果我们的项目要部署到别的服务器,那么可能需要安装依赖文件,所以在项目最终完成后,可以手动创建一个requirements.txt文件,来告诉机器,在最终运行前需要安装一些依赖项.当然,打包成docker包后,可以在dockerfile中配置直接运行pip install -r requirements.txt 就可以啦!



首先导入flask:

```python
from flask import Flask
```

然后创建一个Flask程序

```python
# 记住,这里是双下划线
app = Flask(__name__) 
```

编写一个视图函数

```python
@app.route('/')
def hello_flask():
    return "hello FLASK"
```

然后编写一个程序运行的入口

```python
if __name__ == '__main__':
	app.run(host=0.0.0.0)
```

然后我们就可以运行程序了.访问localhost:5000 flask开发服务器默认使用的机器端口号为5000.

这时我们就能看到一个hello FLASK的语句显示在浏览器中.当然我们可以增加更复杂的功能进去.这就看需要如何定制功能了.

#### 加载网页:

想要加载一个网页,我们需要有一个网页,假设我们已经编写好了一个网页,放在了templates目录下,那么我们就可以通过render_template()函数来渲染这个网页.函数中的第一个参数就是我们的网页文件名,当我们想要把后台的一些数据传递到前端网页时,有几种传递方式,一种是使用jinja2模板的语句,在网页中通过{{param}}的方式获取该值,或者直接由我们后台封装一个Response对象,将一些数据包装进去,返回给调用这个接口的网页也是可以的.这里我们展示一下如何渲染一个静态网页index.html,在视图函数的return语句中

```python
return render_template("index.html")
```

#### 避免硬编码:

为了使程序更易维护,我们都不提倡使用硬编

码方式来编写程序,所以,当我们定义好了一个路由,在其他地方使用这个路由时.不能直接使用这个路由,而是推荐用url_for方法,可以通过从flask包中引入这个函数来进行调用.

参数中通过一个字符串的方式,将原本路由对应的视图函数的名字传给这个函数,来解决路由硬编码

```python
url_for("hello_flask")
```

#### 判断前端请求的方法

​	这里使用一个Flask框架的全局对象request,同样需要引入,可以通过

```python
if request.method == "GET" or request.method == "POST":
    pass
```

#### 请求对象的属性:

form属性:前端页面的表单传递的数据,会被封装进这个属性中,是一个类字典对象.不包含文件数据

args:一般是URL中的数据查询参数,Ajax请求参数也被放进这里.

values: form与args的结合.

cookies, 客户端发送过来的cookies信息.

headers:请求头信息,一般做代理或者是转发的时候,在需要修改时,会修改其中内容,然后重新封装进headers进行请求的转发

data: 当以Flask未知的MIMETYPE类型提交数据时,data属性用于一字飞船形式保存提交的数据

#### 回调接入点:

flask框架为我们提供了三个装饰器函数,用于处理公共逻辑

@app.before_request 在请求之前,会执行这个装饰器函数修饰的函数

@app.after_request 在请求完成且未发生异常时,调用,一旦发生异常,则不嗲用

@app.teaddown_request 不论是否发生异常都会之行的装饰器函数







# Flask-Login模块 用于管理用户登录登出管理回话状态.



#### 关于本模块的学习,详细的参考了https://www.jianshu.com/p/06bd93e21945
这位博主的帖子.大家可以学习.本帖只是参照文章内容根据我自己项目的实际需求做出自己的理解.由于我的项目只有一个用户,添加数据库或者文件都略显麻烦,于是考虑维护一个全局的对象来保证会话id的一致.



#### 我个人觉得使用这个模块的核心就是需要具备以下几点:

- 一个自定义的User类,必须继承自UserMixin类,可以什么都不做,但是最好给这个用户一个user_id,在python3环境下,一定要自己重写get_id()方法.返回一个uuid(),因为在后续使用用户登录时,他的session对新用户的sessionid是要依据这个方法的.而且,要有一个地方来存储这个已经创建的用户,和用户的会话状态,一般是存储在数据库中,方便后续比对.

- 为了安全,我们要设置flask框架的security_key

  ```python
  app.security_key = os.urandom(24)
  ```

- 实现一个登录管理器

  ```python
  login_manager = LoginManager()
  login_manager.session_protection = 'strong'
  login_manager.login_view = 'login'
  login_manager.init_app(app=app)
  ```

   第一行初始化登录管理器对象,第二行,设置session保护级别为强保护,第三行用于在未登录时,访问受保护页面时,会自动跳转回 该值指定的视图函数处理.

  第四行用于在需要时注册一下被管理的flask应用.不必在一开始创建对象时就进行注册.

- 使用本模块最重要的一点就是要实现一个回调函数

  ```python
  @login_manager.user_loader
  def load_user(user_id):
      return User.get(user_id)
  ```

  这里要注意,这个get方法,最主要的一点就是比对在第一次创建用户类后生成的Sessionid和当前session中的session是否一致,一致则返回这个user_id标识的对象.否则,返回一个空对象.关于session的存储,大体就是存储成json文件,或者存到数据库,但是比较重要的点就是可以通过sessionid就能获取到这个session才行.这个是保证用户能够正常回话的一个前提.标识用户已经成功登录了.

- 用户的登录:

  ```python
  login_user(user, remember=True)
  ```

  当我们第一次通过前端页面登录后,后台获取到数据,然后创建第一点中所描述的用户对象,然后给这个用户创建一个user_id,通过我们重写的这个get_id方法,为新用户创建一个user_id.当我们在调用login_user方法的时候,将这个对象作为参数传进去, 然后这个方法会调用对象本身的get_id方法来创建sessionid.所以我们重写上述一点中的get_id时,要做一个判断,假如是一个新用户,要进行用户对象的创建,首次创建对象过程中,直接生成一个新的uuid(这里可以直接用內建的uuid模块来创建),而如果是要进行用户登录,那么这个用户的用户名必然存在,可以根据这个信息来进行验证,表示用户已经登录过了,此时只需建立sessionid即可.返回第一次创建对象过程中创建的uuid给sessionid.

- 用户的登出:

  ```python
  @app.route('/logout')
  @login_required
  def logout():
      logout_user()
      return redirect(url_for('login'))
  ```

  可以像参考链接中的例子一样进行编写.主要是调用logout_user()方法然后,登出以后,将请求重定向到登录界面就行.

- 受保护页面:

  用一个装饰器函数 @login_required 来对想要保护的页面进行修饰,添加该装饰器的视图函数都会在用户未登录时,跳转到 login_manager.login_view = 'login' 这个语句指定的视图函数上去.





# flask + requests 包实现简单的反向代理

在实现反向代理之前:先简单描述一下两种代理方式,以及他们的区别:

参考:https://blog.csdn.net/zt15732625878/article/details/78941268

- #### 正向代理:

  - 位于客户端和内容服务器之间的一个代理服务器,当客户端无法直接访问内容服务器时,就可以通过代理服务器去访问内容服务器.然后这个代理必须是可以访问内容服务器的一个服务器,当代理服务器从内容服务器拿到数据后,再将数据返回给客户端,而此时,内容服务器只认为是代理服务器跟他进行了数据往来,而不知道其实真正的请求是由客户端发起的.
  - 对应到可能的应用场景,就是典型的**`爬虫代理`**,使用的就是正向代理的原理.当用一个ip去不断获取某一个服务器的数据,作为服务器使用者的商家势必要对爬虫程序进行限制,有可能会封掉这个ip,此时为了保证我们本身的ip不会被封掉,我们就可以使用代理ip替我们去请求数据,然后再将数据交给我们.

- #### 反向代理:

  - 也是存在客户端和内容服务器之间的一个代理服务器,但是,它是用来代理内容服务器的,就好像是外交部发言人的角色一样,他代表的是我们国家对外的态度.当客户端想要访问内容服务器,就必须先经过这个反向代理,反向代理可以对这个请求进行管理,可以拒绝,也可以通过.当一个请求在反向代理服务器上被通过了,那么这个代理就会将这个请求的内容,原封不动的转发给内容服务器去获取数据,然后将内容服务器的响应结果返回给客户端..



### flask + requests实现代理:

```python
import requests
from flask import Response, request
@app.route('/revproxy/<path:url>', methods=["GET","POST"])
def revproxy():
    # 假设的内容服务器IP
    content_server = "http://192.168.100.100"
    # 内容所在服务器的内部接口
    url = content_server + url
    # 当收到GET请求,通过requests.get向content_server发起请求
    if request.method == "GET":
        rsp = requests.get(url, params=request.args, headers=request.headers)
        # 这里根据需求,设置响应的返回格式,可自己指定
        return Response(rsp, content_type='application/text')
    if request.method == "POST":
        rsp = requests.post(url, data=request.data, headers=request.headers)
        return Response(rsp, content_type='application/text')
```

​	
