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
            - `--name='containerName'` 或者  `--name containerName` 
            - `-d`: 后台方式运行
            - `-i`: 使用交互式方式运行
            - `-t`: 为容器重新分配一个伪输入终端， 通常与`-i` 混合使用   
            - `-p`: 小写p指定容器端口： `-p 主机端口： 容器端口`
            - `-P`: 大写P指定随机端口
    - 查看容器内运行的进程： `docker top contarinerId`
    - 查看容器的元数据：`docker inspect [OPTIONS] NAME|ID [NAME|ID...]`
    - 进入容器，以命令行交互：
        1. `docker exec -it containerId bashShell`
        2. `docker attach containerId`
        3. 区别：
            - `exec` ：在容器中打开新的终端，并且可以启动新的进程
            - `attach` ： 直接进入容器启动命令的终端，不会启动新的进程 
    
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
               
    - 重用的命令：
        - 后台启动： `docker run -d imageName` 
            - 常见的坑：docker 容器后态启动后，就必须有一个前台进程，docker 发现没有前台进程，就会自动停止
        - 查看日志：`docker logs [OPTIONS] CONTAINER` 
            - `-t`: 显示时间戳
            - `-f`: follow log out 追加输出
            - `--tail 数字`： 显示最后多少条
            - 如： `docker logs -tf --tail 10 CONTAINERID`
        - 查看容器中进程信息: `docker top CONTAINER [ps OPTIONS]`
        
        - 查看容器的元数据：`docker inspect [OPTIONS] NAME|ID [NAME|ID...]`
           
        - 进入容器：
            - `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]`
                - 如： `docker exec -it containerId /bin/bash`
            - `docker attach containerId`
            - 两种方式的区别： 
                1. `exec` ：在容器中打开新的终端，并且可以启动新的进程
                2. `attach` ： 直接进入容器启动命令的终端，不会启动新的进程 
        - 文件copy到主机: 
             - `docker cp 容器id: 容器内路径 目地主机路径`
             - `docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH`
        - 宿主机copy 到容器：
             - `docker cp [OPTIONS] DEST_PATH CONTAINER:SRC_PATH`
            
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
 - 添加数据卷的两种方法：
    - 直接命令添加：`docker run  -v 宿主机绝对路径目录：容器内目录 IMAGENAMEl /bin/bash`
    - Dockerfile:
       ```docker
        FROM centos 
        VOLUME ["dataVolume1","dataVolume2"]    
        CMD echo "finished, success!"
        CMD /bin/bash
       ```      

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



### 制作自己的第一个镜像：

 ```shell script
# 宿主机
docker pull ubuntu
docker run -it ubuntu /bin/bash
docker cp ./jdk-8u261-linux-x64.tar.gz 5cdbb0760fd6:/tmp/
docker cp ./Miniconda3-latest-Linux-x86_64.sh 5cdbb0760fd6:/tmp/
docker cp ./elasticsearch-7.4.2-linux-x86_64.tar.gz 5cdbb0760fd6:/tmp/
docker cp ./kibana-7.4.2-linux-x86_64.tar.gz 5cdbb0760fd6:/tmp/

# 容器内, 配置jdk1.8环境
cd /tmp
mkdir /usr/local/java
tar -zxvf jdk-8u261-linux-x64.tar.gz -C /usr/local/java/
rm jdk-8u261-linux-x64.tar.gz
cd /usr/local/java
mv jdk1.8.0_261 jdk1.8
apt update
apt install vim
vim /etc/profile
    # 复制以下内容到末尾
    # export JAVA_HOME=/usr/local/java/jdk1.8
    # export JRE_HOME=${JAVA_HOME}/jre
    # export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
    # export PATH=.:${JAVA_HOME}/bin:$PATH
source /etc/profile

#容器内， 更换apt 下载源
mv /etc/apt/sources.list /etc/apt/sourses.list.backup
vim /etc/apt/sources.list
    # 添加以下内容
    #  deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
    #  deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
    #  deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
    #  deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
    #  deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
    #  deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
    #  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
    #  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
    #  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
    #  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
bash /tmp/Miniconda3-latest-Linux-x86_64.sh
    # 一路输入yes
    # 开机不自动激活base环境, conda config --set auto_activate_base false
vim ~/.bashrc
    # 末尾加入： export PATH=$PATH:/home/root/miniconda3/bin
source ~/.bashrc
    # 配置conda 源
    # conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
    # conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
    # conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
    # conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda 
    # conda config --set show_channel_urls true
    # 需要的包自定义安装 conda install xxx 
# 容器安装elasticsearch7.6.2


# 容器安装Kibana 7.4.2
# 参考：https://blog.csdn.net/weixin_43249121/article/details/109849886
# 有很多坑：
#   （1）比如容器内无法修改sysctl.conf 之后的sysctl -p ，这个在宿主机修改跨过这一步即可
#    (2) 修改配置文件, 用es 用户启动 
# root : root
# es: es
tar -zxvf elasticsearch-7.4.2-linux-x86_64.tar.gz -C /opt/
adduser es
未完....环境太麻烦了...
# 容器安装 kibana7.4.2

````
