---

---

## 管理Nginx进程

##### 开启web服务:

```shell
service nginx start
```

##### 停止web服务:

```shell
service nginx stop
```

##### 重启web服务:

```shell
service nginx restart
```

##### 如果我们只是简单的进行配置更改,那么Nginx通常可以重新加载而不会丢失连接:

```shell
service nginx reload
```



## 设置服务器块(推荐做法)

​	使用Nginx Web服务器时,可以使用服务器模块来封装配置的详细信息,并从单个服务器托管多个域.

Nginx默认启用了一个服务器模块,这个模块被配置为 在/var/www/html目录下提供文档.适用于单个站点,当站点增多便很笨重,我们要做的就是为另外的站点配置一个独立目录,并保留默认目录,

按如下步骤为example.com创建目录,使用 `-p`标志创建任何必须的父目录

```shell
sudo mkdir -p /var/www/example.com/html
```

接下来使用 `$USER`环境变量分配目录所有权:

```shell
sudo chown -R $USER:$USER /var/www/example.com/html
```

然后随便编写一个html文件放入其中,这个网站就算部署完成了



为了让Nginx提供这些内容,有必要创建一个具有正确指令的服务器块.做法是不要直接修改默认配置文件,而是在/etc/nginx/sites-available 目录下新建一个`example.com`文件

```shell
sudo nano /etc/nginx/sites-available/example.com
```

将配置文件中的内容粘贴到此文件中

```shell
server {
        listen 80;
        listen [::]:80;

        root /var/www/example.com/html;
        index index.html index.htm index.nginx-debian.html;

        server_name example.com www.example.com;

        location / {
                try_files $uri $uri/ =404;
        }
}
```

请注意，我们已将`root`配置更新到我们的新目录，并将`server_name`为我们的域名

但是这样仍然不能让Nginx找到我们的网站,我们还需要让服务器程序知道如何选择那个站点,我们要创建一个链接文件,把他放在nginx下面sites-enable目录下,这样,服务器就可以根据url来相应不同的网站了

```shell
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
```

做完上述的操作,我们就启用了两个服务器模块并将其配置为了基于listen和server_name的指令响应请求:

- example.com: 会响应example.com和www.example.com请求

- default: 会响应端口80上除了上述域名的任何请求.

- 同时,为了避免添加额外的服务器名称可能导致的哈希桶内存问题,有必要调整`/etc/nginx/nginx.conf`文件

  打开文件,找到`server_names_hash_bucket_size`指令并删除`#`符号以取消注释该行：

  ```
  http {
      ...
      server_names_hash_bucket_size 64;
      ...
  }
  ```

- 检测Nginx文件中有无语法错误

- ```shell
  sudo nginx -t
  ```

  若无任何问题便可以直接重启服务,然后进行访问了



## Nginx的主要配置文件以及重要目录

#### 内容

- /var/www/html 默认的服务器站点目录,测试服务器安装以及服务启动是否成功

#### 服务器配置

- `/etc/nginx`: Nginx配置目录. 所有的Nginx配置文件都驻留在这里.
- `/etc/nginx/nginx.conf:主要的Nginx配置文件.可以直接修改,以用于Nginx的全局配置
- `/etc/nginx/sites-available/`:可以存储每个站点服务器块的目录,就是每个站点对应的服务器程序配置.除非Nginx将其中的某一服务器块链接(创建对应文件的链接文件)到了sites-enable目录下,否则,Nginx是不会使用此目录中的配置文件的.通常来说,所有的服务器块配置都是在此目录中完成,然后通过链接到其他目录来启用
- `/etc/nginx/sites-enable`:存储启用的每个站点服务器块的目录.通常,该目录下的文件都是从上面目录中的文件链接得到的.只要是存储在本目录下的链接文件,其内容都是上目录的站点配置,那么Nginx就能根据配置,找到相应的站点
- `/etc/nginx/snippets`:这个目录包含可以包含在Nginx配置其他地方的配置片段

####  服务器日志

`/var/log/nginx/access.log`:除非Nginx配置为其他方式,否则每个对你的WEB服务器的请求都会记录在此日志文件中.

`/var/log/nginx/error.log`:所有的错误信息都被记录在此处