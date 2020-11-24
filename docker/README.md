# docker

[Ubuntu上学习使用Docker](https://blog.csdn.net/P_LarT/article/details/107768318)

## 概念
docker 是一种linux 容器技术。
 - 容器（container）: 正在运行的进程
 - 镜像（image）: 镜像包含运行应用程序所需的所有内容——代码或二进制文件、运行时、依赖项以及所需的任何其他文件系统对象
 - 镜像用来创建容器,是容器的只读模板。
 - 优点：
    - 将一整套环境打包封装成镜像，无需重复配置环境，解决环境带来的种种问题， 速度快。
    - Docker容器间是进程隔离的，谁也不会影响谁
  
 - 个人理解：镜像类比与java中的class, 从镜像启动的容器，相当于new 一个对象
## 安装
    
- [官方文档](https://docs.docker.com/engine/install/ubuntu/)
- [Ubuntu 20.04 中 安装docker](https://blog.csdn.net/luodong1501/article/details/106194408)
-  `sudo apt-get install docker.io`

## 镜像加速配置
 
 - sudo gedit /etc/docker/daemon.json
    - 添加阿里云的个人镜像加速地址
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

3. 容器命令
    - 启动容器: `docker run`
        - 语法： `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`
            - `--name='name'`: 容器名字，如tomcat
            - `-d`: 后台方式运行
            - `-it`: 使用交互式方式运行，进入容器查看内容
            - `-p`: 指定容器端口： `-p 主机端口： 容器端口`
    
    - 查看容器： `docker ps `: 
        - 语法： `docker ps [options]`
            - `-a`: 查看当前正在运行的容器 + 历史运行过的容器
            - `-n=?`: 显示最近创建的容器
            - `-q`: 只显示容器的编号
    - 容器退出：            
        - `exit` : 容器停止并推出
        - `ctrl + p + q`: 容器不停止退出
    
    - 删除容器: `docker rm 容器id`
        - `docker rm -f $(docker ps -aq)`: 删除所有容器 
     
    - 启动和停止容器：
        - `docker start containerId`: 启动容器 
        - `docker restart containerId`: 重启容器 
        - `docker stop containerId`: 停止当前正在运行的容器 
        - `docker kill containerId`: 强制停止当前容器 
               
    - 重用的其他命令：
        - 后台启动： `docker run -d imageName` 
            - 常见的坑：docker 容器后态启动后，就必须有一个前台进程，docker 发现没有前台进程，就会自动停止
        - 查看日志：`docker logs [OPTIONS] CONTAINER` 
            - `-t`: 显示时间戳
            - `-f`: follow log out 追加输出
            - 如： `docker logs -tf --tail 10 CONTAINERID`
        - 查看容器中进程信息: `docker top CONTAINER [ps OPTIONS]`
        
        - 查看容器的元数据：`docker inspect [OPTIONS] NAME|ID [NAME|ID...]`
           
        - 进入容器：
            - `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]`
                - 如： `docker exec -it containerId /bin/bash`
            - `docker attach containerId`
            - 两种方式的区别： 
                1. `exec` 进入新终端， 
                2. `attach` 进入当前正在进行的终端
        - 文件copy:
            `docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH`
 
            
            
## docker 联合文件系统（UnionFS）
 核心思想：文件分层复用

- 提交自己的docker镜像：
    - `docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]`        
        - options:
            1. -a, --author string    Author (e.g., "John Hannibal Smith <hannibal@a-team.com>")
            2. -c, --change list      Apply Dockerfile instruction to the created image
            3. -m, --message string   Commit message
            4. -p, --pause            Pause container during commit (default true)
         - 如： `docker commit -a="dosea" -m="add webapps" ContainerId tomcat_dosea:1.0`
        ```shell script
        docker pull tomcat                                                        # 拉取镜像
        docker run -it -p 8080:8080 tomcat                                        # 启动容器
        docker exec -it ContainerId /bin/bash                                     # 进入容器内
        # update tomcat                                                           # 自定义修改某些内容
        docker commit -a="dosea" -m="add webapps" ContainerId tomcat_dosea:1.0    # 提交自己的容器，打包成镜像                         
        docker images                                                             # 查看，发现自己打包的镜像
        ```
            
## 容器数据卷
 实际就是目录的挂载，实现数据共享。
 
- 使用数据卷
    `docker run -it -v 主机目录：容器内目录 IMAGENAMEl /bin/bash` 




## DockerFile 
1. 基础知识：
        
        1. 每个保留关键字（指令）都必须是大写字母
        2. 执行从上到下的顺序
        3. # 表示注释
        4. 每一个指令都会创建提交一个新的镜像层， 并提交
        
2. 语法： 
    - `FROM` : 指定一个基础镜像, 没有指定tag ，默认为latest
        - `FROM  <image>[:<tag> | @<digest>] [AS <name>]`
        - `FROM scratch`: 表示从头创建镜像，不依赖于base 镜像 
        
    - `MAINTAINER`: 镜像维护者信息 姓名 + 邮箱
        ```docker
        MAINTAINER duhaipeng <duhaipeng@enn.cn>
        ```
              
    - `LABEL`: 给创建的镜像添加标签，比如作者信息，版本信息，描述信息等。
        ```docker
        LABEL maintainer = "作者姓名"
        
        LABEL version = "1.0"
        
        LABEL description = "描述"
        ```
    - `RUN`:执行命令，　镜像中安装一些软件，　每一条RUN都会多一层，尽量把RUN语句合并 `&& \` 
       ```docker
        RUN yum update && \
        yum install -y vim 
       ```
    - `WORKDIR` ： 类似于linux 的cd, 如果没有则会自动创建
        - 对目录操作尽量使用`WORKDIR`, 不要使用`RUN cd`
        - 尽量使用绝对路径
        
       ```docker
        WORKDIR /test   #如果没有会自动创建test目录
        WORKDIR demo    #同上
        RUN pwd         # 输出 /test/demo
       ```
      
    - `ADD`:  将某文件复制到固定目录下, 可以将tar文件解压提取到固定目录下
        ```docker
        ADD test / ADD test.tar.gz /
       ```
    - `COPY`: 将某文件复制到固定目录下， 单纯复制
    
    - `ENV`: 为当前容器设置环境变量
      ```docker
        ENV MYSQL_VERSION 5.7   # 设置常量 MYSQL_VERSION  值是 5.7
      ```
      
    - `CMD`: 容器启动时默认执行的命令, 如果docker run 指定了其他命令，CMD命令被忽略,
        如果定义了多个CMD,只有最后一个CMD会被执行。
    - `ENTRYPOINT`： 
    - `EXPOSE`:　暴露容器运行时的监听端口给外部
    - `VOLUME`:  可实现挂载功能,容器告诉Docker在主机上创建一个目录(默认情况下是在/var/lib/docker),
                然后将其挂载到指定的路径。当删除使用该Volume的容器时,Volume本身不会受到影响,它可以一直存在下去。
                
3. docker build               
    - 语法： `docker build [OPTIONS] PATH | URL | -`
        - `-t`: name:tag
        - `-f`: Dockerfile路径，默认当前路径下的`./Dockerfie`
        - 最后一个为路径, 不要忘记这个参数 一般写当前路径 `.`