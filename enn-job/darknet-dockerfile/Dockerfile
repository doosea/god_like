FROM ubuntu:20.04
MAINTAINER duhaipeng <duhaipeng@enn.cn>

WORKDIR /

COPY darknet /darknet

RUN sed -i "s@http://archive.ubuntu.com@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    sed -i "s@http://security.ubuntu.com@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    apt-get update && DEBIAN_FRONTEND="noninteractive" \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-dev \
        python3-pip \
        build-essential \
        net-tools \
        iputils-ping \
        telnet \
        linux-libc-dev \
        libc6-dev \
        procps \
        vim \
        git \
        curl \
        less \
        tzdata \
        file &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install -U pip -i https://mirrors.aliyun.com/pypi/simple && \
    echo "\nset fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936" >> /etc/vim/vimrc && \
    echo "set termencoding=utf-8" >> /etc/vim/vimrc && \
    echo "set encoding=utf-8" >> /etc/vim/vimrc

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install setuptools wheel && \
    rm -rf /root/.cache/pip/* && \
    cd /darknet && \
    make && \
    ln -s /darknet /usr/lib/python3/dist-packages/darknet

CMD /bin/bash


# sudo docker build -f ./Dockerfile  -t mydarknet:cpu-1.0 .