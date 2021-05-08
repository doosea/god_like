## 图片标注工具调研
参考连接： 
    - [一文了解图像标注类型](https://blog.csdn.net/weixin_42216109/article/details/115430185)
    - [目标检测中的数据标注及格式转换代码](https://zhuanlan.zhihu.com/p/138067316)
    
0. 图像标注概念
    - 图像标注是一个将标签添加到图像上的过程
    - 分类问题：一张图片里面有一个物体，识别出来这个物体是什么，这类问题是分类问题
    - bounding box：一张图片里面有一个或若干个物体，识别出来这个物体是什么，并用框子框出来；
    - 语义分割：一张图片里面有若干个物体，对于图片中的每个像素，判断其属于哪个类别；
    - 实例分割：在语义分割的基础上，判断每个像素属于对应类别的哪个个体；
1. 图片标注类型（5种）
    - 分类标注classification， 表现形式一般就是一张图对应一个数字标签
        - 代表数据集： 猫狗数据集 [Dogs VS Cats](https://mp.weixin.qq.com/s?__biz=Mzg2MDE3NTk5MQ==&mid=2247483854&idx=1&sn=447ccf33a0a94f68395b92a2a169ae01&chksm=ce2b2ad6f95ca3c09df11dc0566611420a2513780b72fe282bee705195e0fc70ac31ca3ea69c&scene=21#wechat_redirect)
        - Dogs vs. Cats是Kaggle的一项竞赛，该竞赛需要编写一种算法来对图像包含狗还是猫进行分类。 训练数据集共包含25,000张猫和狗的图像。
    - 点标注keypoints， 点标注通常用于对图像特征较细致的场景，如人体姿态估计，人脸特征识别等
        - 代表数据集： Leeds Sports Pose， 体育姿势数据集， 分为竞技、羽毛球、棒球、体操、跑酷、足球、排球和网球几类，共包含约 2000 个姿势注释
        - 应用： 口罩检测 [Artificial mask dataset](https://mp.weixin.qq.com/s?__biz=Mzg2MDE3NTk5MQ==&mid=2247483885&idx=1&sn=9634a8468bcbaab621de9a0fc45eb828&chksm=ce2b2af5f95ca3e3c634224e865777ade811f5708e0f39604eef87864cf9107703d231043b54&scene=21#wechat_redirect) 
    - 线标注（line）， 线标注最常用的应用场景就是自动驾驶领域，用来识别车道及边界
    - 边界框（bounding box）， 边界框标注主要用于对象检测，用来识别某个特征在图像中的具体位置
        - 代表数据集 [CALTECH-Airplane detection](https://mp.weixin.qq.com/s?__biz=Mzg2MDE3NTk5MQ==&mid=2247483911&idx=1&sn=ac763c9aa742d833d34597431582fb37&chksm=ce2b291ff95ca0099dbac763cb54fb7e4ce1be2814004eba627f9f7fc61f3ae143bf7eabccba&scene=21#wechat_redirect)
        - 主要用作对象检测。数据集共含有800张飞机类jpg图片，同时含有相应图片中飞机的边界框坐标
    - 像素标注（pixel level label）， 像素标注又称区域标注，是一种将图像中像素进行归类的标注方式，主要有语义分割和实例分割两种
        - 代表数据集： [KolektorSDD](https://mp.weixin.qq.com/s?__biz=Mzg2MDE3NTk5MQ==&mid=2247483758&idx=1&sn=380f495993aa3c61f29267b15c8820f1&chksm=ce2b2a76f95ca360179408036c3b9760477614d1d42b43c4f42083655e42f186df307da5f3a0&scene=21#wechat_redirect)
        - 该数据集由包含缺陷的电子换向器的图像构成, 总共有52张缺陷图像，347张图无缺陷图像。
2.标注之后的文件格式（常用的数据集：PASCAL VOC，  ImageNet， COCO）
    - XML标注格式： PASCAL VOC， ImageNet, 每一张图片对应一个xml格式的标注文件,
        - xml文件中给出了：图片名称、图像尺寸、标注矩形框坐标、目标物类别、遮挡程度和辨别难度等信息。
        - 训练时，要把xml转化为csv文件
    - json 标注格式： COCO
    - YOLO（txt）     
        - YOLO的txt标注文件有两部分组成：类别编号和矩形框坐标
3. 开源好用的图片标注工具调研
    - lableme 等客户端, 本地使用 
    - 在线平台[京东众智](https://biao.jd.com/business/createProject) :
    - 在线平台[阿里PAI](https://help.aliyun.com/product/30347.html)  
4. 一些想法：
    - 是否要全部支持所有标注方式类型
    - 是否仅仅支持线上标注的方式， 开发者本地标注好的数据，能否支持上传成平台    
    - 实现在线web端标注的可行性方案：
        - 1. vue+canvas， 纯前端的实现方式，传给后端数据，后端拼接, 目前AI开发平台的方式
5. 标注格式
    - voc数据集： xml
    - coco : json
    - YOLO等大部分数据集: txt  
        - 格式： [labelID, 中心点X的比例标注, 中心点Y的比例标注, BOX宽比例标注, BOX高比例标注]
6. canvas生成xml
    - {
        "x":337,   
        "y":272,
        "w":37,
        "h":27,
        "scale":1.086046511627907,
        "canvasX":337,
        "canvasY":272,
        "c":"safe",
        "indexRec":1,
        "dpr":1
       }

## AI-vedio 主要接口逻辑
1. 图像标注, 生成 xml, 
    - 接口： /AIClould/ai/api/updataDrawInfo
    - 前端传给后端图片info， 和user标注信息，后端保存到数据， 并在本地生成xml文件（图片标注的产物）
    
2. 模型训练
    - 接口: /AIClould/ai/api/trainStart
    - 逻辑：
        - （1）根据id所有的图片桶数据信息
        - （2）清空一个规定的本地路径下的数据信息( 训练时所用数据 Directory， DirectoryXML, DirectoryMain, DirectoryLabels)
        - （3）再把当前训练任务的数据上传到指定路径下
        - （4）查函数库，所有的标注类型， 拼接成字符串，拼接到py文件并上传, voc_label.py
            - 主要改了class=[]
        -  (5) 修改本地cfg配置文件上传至远程服务器， yolov3-voc.cfg， 替换默认参数中的一些数值
            - 这里是darknet 的训练参数， max_batches， filters， classes
        - （6）修改本地data配置文件上传至远程服务器， voc.data
        - （7）通过执行 python 脚本， 和 linux脚本 ，开启训练任务（起了新线程）  
            - 具体训练逻辑在 MyThread.run() 中         
            - 主要逻辑还是通过执行linux 脚本的方式运行darknet 
            - 训练完，生成模型 .zip存放在/mnt路径
3. 推断流程
    - pass
    
## Darknet 
### 1. [install Darknet](https://pjreddie.com/darknet/install/)
0. YOLO: you only look once , object detection 算法
    - [算法详解](https://blog.csdn.net/u014380165/article/details/72616238)
    - 作者在YOLO算法中把物体检测（object detection）问题处理成回归问题，用一个卷积神经网络结构就可以从输入图像直接预测bounding box和类别概率。
    - 算法首先把输入图像划分成S*S的格子，然后对每个格子都预测B个bounding boxes，每个bounding box都包含5个预测值：x,y,w,h和confidence。
1. Opencv 
    - pass 
2. CUDA  
    - pass
3. 安装darknet
    - git clone https://github.com/pjreddie/darknet.git
    - cd darknet
    - make (修改Makfile中的参数)
        - GPU=1,  GPU 比 CPU 快500倍, -i <index> 选择gpu的卡
            - nvidia-smi 查看 gpu info
            - 如果使用了CUDA 但是仅仅使用CPU, 可以用参数 -nogpu 控制
        - OPENCV=1,  可以支持更多类型的图片方式， 并且 不需要保存到磁盘
### 2. [YOLO: Real-Time Object Detection](https://pjreddie.com/darknet/yolo/)       
1. cfg 下面是一些yolo模型网络参数配置文件          
2. yolov3.weights 是预先训练好的yolo3的网络模型参数  
    1. 检测一张图片, 两种方式相同
        -  ./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg
        -  ./darknet detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights data/dog.jpg
    2. 检测多张图片
        - ./darknet detect cfg/yolov3.cfg yolov3.weights 后面不跟数据路径
        - Enter Image Path:  交互模式输入单个图片路径，检测一张图片后生成 predictions.jpg
    3. 检测图片默认阈值是>0.25的才会显示， 手动改变阈值参数  -thresh <val>
        - ./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg -thresh 0
3. Tiny YOLOv3 小型的yolo框架，层数比较少， 使用方式一样
4. 摄像头上的实时检测 （待完善）
    - 想要完成摄像头的试试检测，必须安装 CUDA 和 Opencv
        - ./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights
        - ./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights <video file>
5. Training YOLO on VOC
    - VOC 的 标注数据是xml格式 ， darknet 需要的是 .txt : <object-class> <x> <y> <width> <height>
        - scripts/voc_label.py 可以完成xml 到txt的转化
    - 自定义cfg for VOC 
        - cfg/voc.data 
            ```
                classes= 20
                train  = <path-to-voc>/train.txt
                valid  = <path-to-voc>/2007_test.txt
                names = data/voc.names
                backup = backup 
            ```
        - 下载pre-trained 权重 darknet53.conv.74
        - ./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg darknet53.conv.74
6. Training YOLO on COCO
    - 使用多块GPU卡训练
        - ./darknet detector train cfg/coco.data cfg/yolov3.cfg darknet53.conv.74 [-gpus 0,1,2,3]
    - 从断点出重新开始接着上次的训练任务
        - ./darknet detector train cfg/coco.data cfg/yolov3.cfg backup/yolov3.backup -gpus 0,1,2,3
    
    
### 3. [imageNet Classification](https://pjreddie.com/darknet/imagenet/)
0. 概念
    -imageNet Classification : 1000 类图片分类任务
1. 使用demo
    - ./darknet classifier predict cfg/imagenet1k.data cfg/darknet19.cfg darknet19.weights data/dog.jpg
        - 分类任务中的预测 classifier predict
        - 使用的是 darknet19 的网络结构
        - pre-trained 网络权重 ： darknet19.weights 
    
### 4. [RNN in darknet](https://pjreddie.com/darknet/rnns-in-darknet/)
1. 训练demo
    - ./darknet rnn train cfg/rnn.train.cfg -file data.txt
    - ./darknet rnn train cfg/rnn.train.cfg backup/rnn.train.backup -file data.txt
    
### 5. [DarkGo](https://pjreddie.com/darknet/darkgo-go-in-darknet/)
1. 类似与alphaGO
    - ./darknet go test cfg/go.test.cfg go.weights
### other 


### darknet python API 
0. 参考连接：
    - [YOLOV3实战3：用python调用Darknet接口处理视频](https://blog.csdn.net/phinoo/article/details/83009061)
    - [darknet yolov4 python接口测试图像](https://blog.csdn.net/LEILEI18A/article/details/107281540)
    - 修改了c端的源码
1. 值得思考的问题：
    - 怎么把 darknet 转化给user 使用
    - python API 足以支持这么多 darknet 的使用场景吗
    - python API how to use
 
##  DockerDarknet
0. 概念： darknet 的 docker 部署
    - cpu： Central Processing Unit 中央处理器， CPU擅长逻辑控制，是串行计算
    - gpu: Graphics Processing Unit 图像处理器， GPU擅长高强度计算，是并行计算
    - nvidia： 显卡的类型品牌
    - cuda:  NVIDIA推出的用于自家GPU的并行计算框架， CUDA只能在NVIDIA的GPU上运行
    - cudnn: CUDA Deep Neural Network library， 是NVIDIA打造的针对深度神经网络的加速库
    
1. cuda 官方镜像
    - base: 基于CUDA，包含最精简的依赖，用于部署预编译的CUDA应用，需要手工安装所需的其他依赖。
    - runtime: 基于base，添加了CUDA toolkit共享的库
    - devel: 基于runtime，添加了编译工具链，调试工具，头文件，静态库。用于从源码编译CUDA应用。
    
2.  准备 Docker 镜像
    - [Docker: Nvidia Driver, Nvidia Docker 推荐安装步骤 ](https://mp.weixin.qq.com/s/fOjWV5TUAxRF5Mjj0Y0Dlw)
        - 安装 Nvidia Driver （需要注意 cuda 版本问题）
            - ubuntu-drivers devices：　查看推荐的NVIDIA显卡驱动版本
            - sudo apt install nvidia-driver-XXX #XXX为4.1结果中显示的具体版本号
        - 安装docker
        - 安装nvidia docker
3. 构建镜像
    1. nvidia/cuda 镜像， docker hub 官网提供官方版本作为基础镜像
        - docker pull nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04
    2. OpenCV
        - 基于 nvidia/cuda 镜像，构建 OpenCV 的镜像
        - docker pull joinaero/ubuntu18.04-cuda10.2:opencv4.4.0
    3. Darknet
        - 基于 OpenCV 镜像，构建 Darknet 镜像
        - docker pull joinaero/ubuntu18.04-cuda10.2:opencv4.4.0-darknet
4. CPU-darknet 镜像构建
```dockerfile
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
    make

CMD /bin/bash
```   
    - 制作镜像： `sudo docker build -f ./Dockerfile -t darknet-cpu:1.0 .`
    - 启动容器： `sudo docker run --name mydarknet-cpu -v /mydata/yolo:/darknet/mydata -it darknet-cpu:1.0 bash`
    - 测试darknet使用：
        - `cd darknet`
        - `./darknet detector test ./cfg/coco.data ./cfg/yolov3.cfg /mydata/yolo/yolov3.weights data/dog.jpg  -thresh 0.25`

   

