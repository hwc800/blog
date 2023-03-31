## 上线配置

##### 1. 修改settings配置

```python
DEBUG = False
ALLOWED_HOSTS = ['*']
```



##### 2. 收集项目静态文件

当Django运行在**生产环境**时，将**不再提供静态文件的支持**，需要将**静态文件交给静态文件服务器**。

我们需要收集项目中静态文件，并放到静态文件服务器中。

我们使用Nginx服务器作为静态文件服务器。

1. 收集项目静态文件

   1. 配置收集静态文件存放的目录

      ```python
      STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
      ```

   2. 执行收集静态文件命令

      ```python
      python3 manage.py collectstatic
      ```

2. 部署Nginx服务器提供静态数据

   1. 查看nginx.conf 目录中 inlcude文件的位置，一般是conf.d 目录。 在conf.d目录新建配置文件`axf.conf`

   2. 配置如下

      ```python
      server { 
              listen       80;
              server_name  线上的域名;
              location /static {
                  alias /Users/apple/Desktop/demo/static;
              }
      }
      ```

      注意：alias 后面的路径是 收集的静态文件存放位置的 绝对路径

   3. 启动Nginx服务器

      如果没有启动，先启动，命令： /usr/local/nginx/sbin/nginx

      如果启动了，重启，命令：/usr/local/nginx/sbin/nginx -s reload

      ```shell
      # 检查配置文件
      $ sudo /usr/local/nginx/sbin/nginx -t
      # 首次启动
      $ sudo /usr/local/nginx/sbin/nginx
      # 重启
      $ sudo /usr/local/nginx/sbin/nginx -s reload
      # 停止
      $ sudo /usr/local/nginx/sbin/nginx -s stop
      ```






##### 3. gunicorn服务

1. 安装gunicorn和gevent包

   ```python
   pip install gunicorn gevent
   ```

2. 在项目主应用目录中(也就是settings.py所在的目录)， 创建 gunicorn-config.py 文件

   ```python
   from multiprocessing import cpu_count
   
   bind = ["127.0.0.1:9999"]  # 注意：上线的项目需要使用 服务器 内网的 ip 地址
   daemon = True  # 是否开启守护进程模式
   pidfile = 'logs/gunicorn.pid'
   
   workers = cpu_count() * 2  # 工作进程数量
   worker_class = "gevent"  # 指定一个异步处理的库
   worker_connections = 65535
   
   keepalive = 60  # 服务器保持连接的时间，能够避免频繁的三次握手过程
   timeout = 30
   graceful_timeout = 10
   forwarded_allow_ips = '*'
   
   # 日志处理
   capture_output = True
   loglevel = 'info'
   errorlog = 'logs/gunicorn-error.log'
   
   ```

   **注意**：

   1，bind 配置中的IP  是 线上 服务器 的内网ip 地址

   2，需要 在 项目根目录中 创建 logs 文件夹

   

3. 开启`gunicorn服务器`

   ```python
   gunicorn -c ./axf2001/gunicorn-config.py axf2001.wsgi
   gunicorn -w 2 myweb.wsgi:application -b 9.135.94.3:8080
           
   重启：
   # 查询与gunicorn相关的所有进程，以进程树形式显示
   pstree -ap|grep gunicorn
   kill -HUP 13741 //重启命令
   ```

4. 修改 axf.conf 配置文件

   ```python
   server {
       listen 80;
       server_name 线上的域名;
     
       location /static {
            alias /Users/apple/Desktop/demo/static;
       }
   
       location / {
           proxy_pass http://127.0.0.1:9999;
           proxy_set_header Host $host;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

5. 重启 nginx 服务器

```
docker 安装  yum install docker
启动docker： systemctl start docker
systemctl enable docker.service  将服务配置成开机启动
systemctl is-enabled docker.service  检查服务是否开机启动
停止docker： systemctl stop docker
systemctl start docker.service  启动服务
systemctl stop docker.service  停止
systemctl disable docker.service 禁止开机启动
systemctl restart docker.service  重启
docker images 查看所有本地镜像
docker rmi 镜像id/镜像名:tag 删除本地镜像
访问 https://hub.docker.com/ 查找想要安装的镜像 使用 docker pull 镜像名:tag 进行拉取
docker pull mysql:5.7 拉取镜像
docker run -p 3305:3306 --name mysql_one -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7  创建容器
docker ps 查看当前运行的容器
docker exec -it mysql_one  bash
docker start 容器id
```

```
第四步开启远程访问权限

命令：use mysql;

命令：select host,user from user;

命令：ALTER USER ‘root’@’%’ IDENTIFIED WITH mysql_native_password BY ‘123456’;

命令：flush privileges;
```

