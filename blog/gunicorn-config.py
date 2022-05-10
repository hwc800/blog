

from multiprocessing import cpu_count

bind = ["10.0.4.15:8000"]  # 注意：上线的项目需要使用 服务器 内网的 ip 地址
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

