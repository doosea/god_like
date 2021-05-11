# kubernetes 

-[k8s笔记参考](https://gitee.com/moxi159753/LearningNotes/tree/master/K8S)

## 架构组件
1. master node
    - Api server: 集群统一入口， 以restful方式，3
    - scheduler：  
    - controller-manager 处理集群中常规后台任务， 一个资源对应一个控制器
    - etcd : 存储系统，用于保存集群相关的数据
2. worker node
    - kubeelet: master 派 到
    - kube-proxy:  
    

# jupyterlab + k8s 调研
1. 参考文档：
    - [Jupyter生态二次开发系列](https://blog.51cto.com/slaytanic/2523291)
    
2. jupyterhub 登录默认的是使用 PAM验证的方式，也就是linux 用户密码方式。 逻辑主要在`jupyterhub/handlers/login.py`
    - SSO: single sign on 单点登录    ----[SSO](https://www.jianshu.com/p/75edcc05acfd)
    - 
    
3. 开发问题：
    - cpu / gpu 资源分配问题
    - 用户的登录鉴权问题
    - 容器之间的数据共享问题
    
4. k8s 部署 jupyterhub： Z2JH
    1. 部署k8s + helm 包管理工具
    2. 安装jupyterhub
        1. 准备配置文件
            -  openssl rand -hex 32： 生成一个随机的32位16进制的
        2. 创建config.yml 配置文件
            - vim config.yml
                ```
                 proxy:
                    secretToken: "<RANDOM_HEX>"
                ```
        3.  添加jupyterhub 仓库地址 并更新helm
            - helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
            - helm repo update    
        4. 使用helm 安装jupyterhub
            ```
               helm upgrade --cleanup-on-fail \
                  --install $RELEASE jupyterhub/jupyterhub \
                  --namespace $NAMESPACE \
                  --create-namespace \
                  --version=0.10.6 \
                  --values config.yaml 
            ```
  
  

# jupyter
1. 两个工程：
    - jupyterhub: （置于JupyterLab前的负责鉴权、启动JuypterLab实例、分发请求（代理）的程序。）
    - jupyterlab： （NoteBook的升级版，专注于Notebook功能，是新一代的Jupyter Notebook）

## jupyterhub
1. 主要由四部分组成
    - hub
    - configurable http proxy 
    - 由spawners 负责的多个，单用户使用的jupyterNoteBook server
    - 鉴权
2. 




