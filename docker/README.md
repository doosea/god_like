# docker

[Ubuntu上学习使用Docker](https://blog.csdn.net/P_LarT/article/details/107768318)

## 概念

 - 容器（container）: 正在运行的进程
 - 镜像（image）: 镜像包含运行应用程序所需的所有内容——代码或二进制文件、运行时、依赖项以及所需的任何其他文件系统对象
 - 镜像用来创建容器,是容器的只读模板。
 - 优点：
    - 将一整套环境打包封装成镜像，无需重复配置环境，解决环境带来的种种问题， 速度快。
    - Docker容器间是进程隔离的，谁也不会影响谁

## 安装
    
- [官方文档](https://docs.docker.com/engine/install/ubuntu/)
- [Ubuntu 20.04 中 安装docker](https://blog.csdn.net/luodong1501/article/details/106194408)
-  `sudo apt-get install docker.io`

## 镜像加速配置
 
 - sudo gedit /etc/docker/daemon.json
 - sudo systemctl daemon-reload
 - sudo systemctl restart docker 

## docker 命令
1. 帮助命令：
    - `docker version`: 查看版本
    - `docker info` : 查看详细信息
    - `docker --help`

2. 镜像命令
    - `docker images`: 列出本地主机上的镜像
        - `-a`: 列出本地所有镜像
        - `-q`: 只显示镜像ID
        - `--digests`: 显示镜像的摘要信息
        - `--no-trunc`: 显示完整的镜像信息

    - `docker search` 
        - 语法：` docker search [options] 镜像名字`
        - options:
            - `--no-trunc`: 显示完整的镜像信息
            - `-automated`: 只列出 `automated build` 类型的镜像
            - `-s`: 列出收藏数不小于指定值的镜像
            
    - `docker pull` ： 从仓库中拉取镜像到本地
        - 语法: `docker pull [OPTIONS] NAME[:TAG|@DIGEST]`         
            - `NAME` :  如 `docker pull ubuntu` , 不指定标签,`:latest`作为默认标签拉取镜像。
            - `NAME:TAG` : 如 `docker pull ubuntu:14.04`， 指定某个版本tag
            - `NAME@DIGEST` : 如`docker pull ubuntu@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`, 
                指定特定版本镜像
                        
    - `docker rmi 镜像名字ID` ： 删除某个镜像


