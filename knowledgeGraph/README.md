# 知识图谱学习

参考连接：
- [awesome-knowledge-graph](https://github.com/husthuke/awesome-knowledge-graph)
- [问答机器人](https://github.com/pengyou200902/Doctor-Friende)

## 1. 简介
1. 什么是知识图谱
    - 知识图谱是由一条条知识组成，每条知识表示为一个SPO三元组(Subject-Predicate-Object)。
2. 知识图谱的数据 
    - NLP 命名实体识别NER，抽取实体
3. 知识图谱的常用技术点：
    - 命名实体识别: NER， 给词打上标签
    - 关系抽取： 基于实体与关系构建知识图谱网络图
    - 实体统一
    - 指代消除
    

## 2. neo4j 图数据库
[neo4j 教程](https://www.w3cschool.cn/neo4j/)
1. 安装: [Linux安装Neo4j](https://www.jianshu.com/p/ef013642a263)
2. 登录：
    第一次启动，默认用户名和密码
        - username: neo4j
        - password: neo4j
        - 修改密码
进入neo4j安装目录的bin文件夹下    
     - 启动：./neo4j start
     - 查看状态：./neo4j status
     - 停止 ： ./neo4j stop
     - 访问： http://localhost:7474/
 
3. neo4j 语法 CQL: Cypher Query Language
    - 基本概念：节点Node， 属性property， 边Relationship
    - CQL 语法 
        1. 增: create(n:Person {name:"dosea", age:18})
            ``` 
           CREATE (adam:User { name: 'Adam' }),
                    (pernilla:User { name: 'Pernilla' }),
                    (david:User { name: 'David'}),
                    (adam)-[:FRIEND]->(pernilla),(pernilla)-[:FRIEND]->(david) 
            ``` 
        2. 删: 
        3. 改
        4. 查 

4. py2neo 连接neo4j
    - [py2neo 使用教程](https://www.jianshu.com/p/febe8a248582)
        ```python
        # 连接数据库
        from py2neo import Graph,Node,Relationship
        graph = Graph("http://localhost:7474",auth=("neo4j","password")) 
        ```
   
    - 创建node 和relationship
        ```python
        a = Node("Person", name="Alice")
        b = Node("Person", name="Bob")
        ab = Relationship(a, "KNOWS", b)
        graph.create(ab) 
      
        # Node和Relationship可以定义对应的实例，Node第一个参数是label, 再利用graph.create()创建
        ```

    - 数据对象 Object
        1. Node: node是保存在Neo4j里面的数据储存单元，在创建好node后，我们可以有很多操作
            ```
            #获取key对应的property
            x=node[key] 
            #设置key键对应的value，如果value是None就移除这个property
            node[key] = value
            #也可以专门删除某个property
            del node[key]
            #返回node里面property的个数
            len(node)
            #返回所以和这个节点有关的label
            labels=node.labels
            #删除某个label
            node.labels.remove(labelname)
            #将node的所有property以dictionary的形式返回
            dict(node) 
            ```
        2. Relationship
            ```
            #创建Relationship
            Relationship`(*start_node*, *type*, *end_node*, ***properties*)
            #返回Relationship的property
            Relationship[key]
            #删除某个property
            del Relationship[key]
            #将relationship的所有property以dictionary的形式返回
            dict(relationship) 
            ```
        3. Subgraphs：子图是节点和关系不可变的集合,我们可以通过set operator来结合，参数可以是独立的node或relationships
            ```
            subgraph | other | ...      结合这些subgraphs
            subgraph & other & ...   相交这些subgraphs
            subgraph - other - ...     不同关系
            #比如我们前面创建的ab关系
            s = ab | ac 
            ```
    - 查询 Query
    - 更新 Update
    
5. 三元组的抽取
    1. 步骤： 
        - 语料字符串，拆分句子
        - 每句话分词
        - 依存句法分析
        - 语义角色构建
        - A0, A1, A2 构建三元组
    2. 实现
        - 使用哈工大:pyltp
        
--------------2020-12-9 更新----------------------
这里不建议用ltp做三元组抽取，最近学习了一个深度学习模型进行三元组抽取  在我的另一个仓库

[链接](https://github.com/shawroad/NLP_pytorch_project/tree/master/relation_extraction/lstm_cnn_information_extract)


--------------2020-11-28 更新----------------------
迪哥使用的是pyltp。 这里我不推荐用pyltp，这个包目前已经不更新了。已经是老古董了。加载的模型估计也过时了。

这里我推荐使用ltp

安装: pip install ltp -i https://pypi.douban.com/simple/

测试安装成功与否: from ltp import LTP

安装成功后   下载模型 直接执行下面的代码  就可以下载了
from ltp import LTP
ltp = LTP()    # ltp = LTP(path = "base|small|tiny") 可以指定参数  默认下载的是small  180m左右


这些操作完成以后  建议先看看ltp的使用方法
可以看代码  ltp的使用.py  或者看官方文档:http://ltp.ai/docs/quickstart.html
然后在去看三元组的抽取  