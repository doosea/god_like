# jupyterhub on kubernetes
- [jupyterhub](https://jupyterhub.readthedocs.io/en/stable/installation-guide-hard.html#part-1-jupyterhub-and-jupyterlab)
## jupyterhub Tutorial
### 1. Installation
- jupyterhub 支持部署在linux, 官方不支持和维护在windows部署方案
1. 安装 JupyterHub and JupyterLab
    -  安装jupyterhub 虚拟环境
        - sudo python3 -m venv /opt/jupyterhub/
    - 激活jupyterhub虚拟环境
        - source /opt/jupyterhub/bin/activate
    - 安装依赖包
        - pip install wheel
        - pip install jupyterhub jupyterlab
        - sudo apt install nodejs npm
        - sudo npm install -g configurable-http-proxy
2. 为 jupyterhub 创建配置文件 ( /opt/jupyterhub/etc/jupyterhub/jupyterhub_config.py)
    - sudo mkdir -p /opt/jupyterhub/etc/jupyterhub/
    - cd /opt/jupyterhub/etc/jupyterhub/
    - sudo /opt/jupyterhub/bin/jupyterhub --generate-config   
3.  设置 systemd 服务
    - sudo mkdir -p /opt/jupyterhub/etc/systemd
    - vim /opt/jupyterhub/etc/systemd/jupyterhub.service
        ``` 
        [Unit]
        Description=JupyterHub
        After=syslog.target network.target
        
        [Service]
        User=root
        Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/opt/jupyterhub/bin"
        ExecStart=/opt/jupyterhub/bin/jupyterhub -f /opt/jupyterhub/etc/jupyterhub/jupyterhub_config.py
        
        [Install]
        WantedBy=multi-user.target
        ```
    - 创建软链接， 放在/etc/systemd/system/ 目录下
        - sudo ln -s /opt/jupyterhub/etc/systemd/jupyterhub.service /etc/systemd/system/jupyterhub.service
    - 刷新systemd的守护进程 ： sudo systemctl daemon-reload
    - 设置jupyterhub.service 开机自动启动： sudo systemctl enable jupyterhub.service
    - 手动启动停止，获取状态
        - sudo systemctl start jupyterhub.service
        - sudo systemctl stop jupyterhub.service
        - sudo systemctl status jupyterhub.service
4. 安装conda 环境对所有的用户
5. 配置nginx 方向代理服务器

### 2. Get Started
1. 配置configuration
    1. 生成默认配置 （jupyterhub_config.py）
        - jupyterhub --generate-config
    2. 启动jupyterhub 服务 以指定的配置文件
        - jupyterhub -f /path/to/jupyterhub_config.py
    3. 理论上所有的参数都可以在命令行配置
    4. DockerSpawner 
2. 6d787d0abeb4415abbc67c44738f423b    
    
### 3. Technical Reference
1. 鉴权机制 Authenticators
    - PAM(Pluggable Authentication Module)  默认使用

### 4. 


# k8s 
0. 概念
    - minikube : 单机版的Kubernetes
    - kubectl 
1. 交互式进程
    - minikube version
    - minikube start
    - kubectl version 