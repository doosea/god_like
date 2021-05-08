# ElasticSearch 

## docker install es and kibana
    
1. 拉取镜像
    - `docker pull elasticsearch:7.4.2`： 存储和检索数据
    - `docker pull kibana:7.4.2` ： 可视化检索数据
2. 创建文件夹，以供挂载
    - `mkdir -p /mydata/elasticsearch/config`
    - `mkdir -p /mydata/elasticsearch/data`
    
3. 写入配置：
    - `echo "http.host: 0.0.0.0" >> /mydata/elasticsearch/config/elasticsearch.yml`  
    
4. 启动es容器

        docker run --name es -p 9200:9200 -p 9300:9300 \
        -e ES_JAVA_OPTS="-Xms1g -Xmx1g" \
        -e "discovery.type=single-node" \
        -v /mydata/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
        -v /mydata/elasticsearch/data:/usr/share/elasticsearch/data \
        -v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
        -d elasticsearch:7.4.2 
        
        启动时遇到的问题：
            - `docker ps` 不显示， `docker logs containerId` 也无日志
            - 修改/mydata/elasticsearch 权限 ： `chmod -R 777 /mydata/elasticsearch` 
            - `curl localhost:9200` : 显示 You Know, for Search 
5. 启动kibana
    
        docker run --name kibanaHome -e ELASTICSEARCH_HOSTS=http://192.168.0.108:9200 -p 5601:5601 -d kibana:7.4.2
        docker run --name kibanaENN -e ELASTICSEARCH_HOSTS=http://10.4.93.246:9200 -p 5601:5601 -d kibana:7.4.2
        踩坑日记：
            - 设置ELASTICSEARCH_HOSTS时， 不应该设置成`localhost`,应该设置成宿主机的ip地址。
            - 解决Kibana启动失败：Data too large问题 
                参考： (http://www.voidcn.com/article/p-vakppzwu-byz.html)
                  （1）在启动es docker是，设置堆内存尽量大一点  `-e ES_JAVA_OPTS="-Xms1g -Xmx1g"`
                  （2）编辑/mydata/elasticsearch/config/elasticsearch.yml 
                    # 缓存回收大小，无默认值
                    # 有了这个设置，最久未使用（LRU）的 fielddata 会被回收为新数据腾出空间
                    # 控制fielddata允许内存大小，达到HEAP 20% 自动清理旧cache
                    indices.fielddata.cache.size: 20%
                    indices.breaker.total.use_real_memory: false
                    # fielddata 断路器默认设置堆的 60% 作为 fielddata 大小的上限。
                    indices.breaker.fielddata.limit: 40%
                    # request 断路器估算需要完成其他请求部分的结构大小，例如创建一个聚合桶，默认限制是堆内存的 40%。
                    indices.breaker.request.limit: 40%
                    # total 揉合 request 和 fielddata 断路器保证两者组合起来不会使用超过堆内存的 70%(默认值)。
                    indices.breaker.total.limit: 95%
            - 容器启动后，修改容易的配置参数
                    - [容器启动后，修改容易的配置参数](https://goodmemory.cc/how-to-modify-the-docker-run-parameters/)
                    - 先停止容器
                    - 停止docker: systemctl stop docker
                    - 修改配置文件，配置文件路径为/var/lib/docker/containers/容器ID，对应的配置文件为hostconfig.json和config.v2.json
                    - 启动docker: systemctl start docker
                    - 启动容器
                    - 注意，重启docker很重要，否则修改完的配置文件，重启容器后会被还原 
6. 启动head 插件
        
        docker pull mobz/elasticsearch-head:5
        docker run -d --name es-head -p 9100:9100 mobz/elasticsearch-head:5
        
        (1)出现跨域问题的解决办法：
            进入es 容器, 修改elasticsearch.yml ， 添加：
                http.cors.enabled: true
                http.cors.allow-origin: "*"
            退出容器,重启
        (2)head 数据浏览部分显示为空白：
            参考：（https://blog.csdn.net/weixin_42830314/article/details/108316045）

## Elasticsearch 初步检索
    
        mysql 数据库的增删改查是靠SQL语法“select * from table where XXX”
        es 增删改查是通过Restful 风格的API进行操作
1. _cat:            
    - `curl localhost:9200/_cat/nodes` : 查看结点
    - `curl localhost:9200/_cat/health` : 查看健康信息
    - `curl localhost:9200/_cat/master` : 查看主结点
    - `curl localhost:9200/_cat/indices` : 查看索引
2. 索引一个文档（保存）

              `es`   : 保存一个数据， 保存在哪个索引的哪个类型下，指定用哪个唯一标识
        类比于 `mysql`: 保存一个数据， 保存到哪个数据库的哪个表格下
    - `PUT index/type/id`: 
        - `PUT` 请求必须带有id， 新增或者修改
    - `POST index/type`: 永远都是新增数据
        - `POST index/type/id`: 新增或者修改
3. 查询数据
    - `GET index/type/id`

4. 更新文档
    - `POST index/type/id/_update`
        - `post`带_`update`： 会对比原来数据，语法里要有`doc`,两次更新不变的话，不会更新版本和序列号；
        - `post`不带`_update`，不会检查原数据；   
    - `put `和 `post `不带_update都会直接更新数据

5. 删除
    - `DELETE index/type/id`： 删除唯一文档
    - `DELETE index`： 删除索引
    
6. bulk 批量API   
    - 语法格式： 
    
            {action: {metadata}}
            {request body}
            {action: {metadata}}
            {request body}
            
            example1: 
                POST /index_1/type_1/_bulk
                {"index": {"_id":"1"}}
                {"name":"dosea1"}
                {"index": {"_id":"2"}}
                {"name":"dosea2"}
                
7. 样本测试数据
        
        POST /bank/acoount/_bulk
         - 'https://github.com/elastic/elasticsearch/edit/master/docs/src/test/resources/accounts.json'
         - account.json 官方测试样例

## ElasticSearch  进阶检索
   `docker update containerId --restart=always`: 设置容器自动重启

1. searchApi： `_search`
    - 方式一(URI Search)： 所有的检索条件放在url后面
    
            GET /bank/_search?q=*&sort=account_number:asc
    - 方式二(Query DSL)： 所有的检索条件放在请求体里
             
             GET /bank/_search
            {
              "query": {
                "match_all": {}
              },
              "sort": [
                {
                  "account_number": "asc"
                }
              ]
            }
2. Query DSL（Domain Specific Language， 领域特定语言） 
   - 参考链接： 
   [Elastic Search之Search API(Query DSL)、字段类查询、复合查询](https://blog.csdn.net/fanrenxiang/article/details/86477019)       
    1. 基本语法格式：
            
            一个查询语句的典型结构：
            {
                QUERY_NAME: {
                    ARGUMENT: VALUE,
                    ARGUMENT: VALUE,...
                }
            }
            针对某个字段的查询结构
            {
                QUERY_NAME: {
                    FIELD_NAME: {
                        ARGUMENT: VALUE,
                        ARGUMENT: VALUE,...
                    }
                }
            }
    2. Query DSL以_search为endpoint，主要分为字段类查询和复合查询
        - 字段类查询： 
            - 单词匹配(Term Level Query)：不对查询语句进行分词处理，直接匹配该字段的倒排索引
            - 全文匹配(Full Text Query)： 对指定的text类型的字段进行全文检索，会先对查询语句进行分词处理
                - `match`、`match_phrase`、`query_string`、`simple_query_string`
                
        - 复合查询： 复合查询就是指可以对多个字段过滤筛选，类比mysql的where多条件查询
            - es的复合查询包括`Constant Score Query`、`Bool Query`、`Dis Max Query`、`Function Score Query`、`Boosting Query`
          
          
          
## Lucene     
    - [Lucene_简介 ](https://blog.csdn.net/Regan_Hoo/article/details/78802897)   
    - [Lucene_原理](https://www.cnblogs.com/huangting/p/11469259.html)
    - [Lucene介绍与使用](https://blog.csdn.net/weixin_42633131/article/details/82873731)
1. 倒排索引（invertedindex）
    - [什么是倒排索引](https://www.cnblogs.com/zlslch/p/6440114.html)



## elasticsearch 

1. 索引操作
    1. 创建索引： `PUT /indexname` (注意索引name 必须为全部小写字母)
    2. 查看所有索引： `GET /_cat/indices`   
    3. 查看单个索引： `GET /indexname`
    4. 删除索引名： `DELETE /indexname`
    5. 删除所有索引： `DELETE /*`

2. 创建索引（index）类型（type）映射（mapping）
    - `mapping-type`: `text`, `keyword`, `date`, `integer`, `long`, `double`, `boolean`, `ip`
    -  查看索引名和mapping： `GET /indexname/_mapping/typename` ， typename 可不写
        ```text
       # indexname=ems, typename=emp
       PUT /ems
        {
          "mapping": {
            "emp": {
              "properties": {
                "id": {
                  "type": "keyword"
                },
                "name": {
                  "type": "keyword"
                },
                "age": {
                   "type": "integer"
                },
                "bir": {
                   "type": "date"
                }
              }
            }
          }
        }
        ```
   
3. 文档操作
    1. 添加文档：
        - `PUT /indexname/typename/id {json_obj}`
        - `POST /indexname/typename {json_obj}`
    2. 查询文档：
        - `GET /indexname/tpyename/id`
    3. 删除文档：
        - `DELETE /indexname/typename/id`
    4. 更新文档
        - `POST indexname/typename/id/_update`
            - `post`带`_update`： 会对比原来数据，语法里要有`doc`,两次更新不变的话，不会更新版本和序列号；
            - `post`不带`_update`，不会检查原数据；   
        - `put `和 `post `不带_update都会直接更新数据
    

## es demo

1. 建立索引mapping
    ```
    PUT /movie
    {
      "mappings": {
        "properties": {
          "name":{
            "type": "text"
          },
          "director":{
            "type":"text",
            "index": false
          },
          "release_date":{
            "type":"date",
            "index": false
          },
          "actors":{
            "type":"text"
          },
          "description":{
            "type": "text"
          },
          "url":{
            "type":"keyword",
            "index": false
          }
        }
      }
    }
    ```




## 安装ik 分词器
- `https://github.com/medcl/elasticsearch-analysis-ik` 招到对应版本 `elasticsearch-analysis-ik-7.4.2.zip`
- 下载解压到容器内部的`plugins` 目录下（在外部挂载之后，放在挂载目录下，不需要进入容器）
- 使用 `elasticsearch-plugin list` 查看已安装的插件
- 重启 `es` 和 `kibana` 容器


# Elasticsearch 原理
[elasticsearch](https://www.elastic.co/guide/cn/elasticsearch/guide/current/intro.html)
## 1. 基础入门
1. 集群内部原理
    - `节点`: 一个运行中的 Elasticsearch 实例称为一个节点。
    - `es集群`: 集群是由一个或者多个拥有相同 cluster.name 配置的节点组成， 它们共同承担数据和负载的压力。
       - `主节点`： 负责管理集群范围内的所有变更，例如增加、删除索引，或者增加、删除节点等。
    - `索引`： 保存相关数据的地方,实际上是指向一个或者多个物理 `分片` 的 逻辑命名空间
    - `分片` : 一个分片是一个 Lucene 的实例, 它本身就是一个完整的搜索引擎
        - `主分片`： 索引内任意一个文档都归属于一个主分片，所以主分片的数目决定着索引能够保存的最大数据量。
        - `副本分片`： 一个副本分片只是一个主分片的拷贝。副本分片作为硬件故障时保护数据不丢失的冗余备份，并为搜索和返回文档等读操作提供服务。
            ```
            设置一个索引的分片数量，                        可以动态调整副本分片数目 
            PUT /blogs                                  PUT /blogs  
            {                                            {
               "settings" : {                               "settings" : {
                  "number_of_shards" : 3,                      
                  "number_of_replicas" : 1                      "number_of_replicas" : 2
               }                                             }
            }                                            }
            ``` 
    - `集群健康`: GET /_cluster/health
        - green： 所有的主分片和副本分片都正常运行。
        - yellow： 所有的主分片都正常运行，但不是所有的副本分片都正常运行
        - red： 有主分片没能正常运行。
        
    - `扩容`: es 集群增加节点，分片（主分片+副本分片）均匀分配到所有节点，每个节点的硬件资源（CPU, RAM, I/O）将被更少的分片所共享，每个分片的性能将会得到提升 
    - `应对故障`： 如果主节点故障， 先从其他节点选取一个当作主节点。 故障节点上的主分区，由其余节点的副本分片代替，升级为主分片。此时，状态由red ==> yellow
    
2. 数据输入与输出
    
    - `文档元数据` 
        - `_index`: 文档的索引
        - `_type`: 文档类型（6.X之后废弃，默认为 _`doc`）
        - `_id`: 文档的唯一标识
        - 一个文档的 _index 、 _type 和 _id 唯一标识一个文档
        
    - 索引文档: 文档存入es， 存储和使文档可被搜索
    - 检索文档：查询es
    - 取回多个文档： _mget
    - 批量操作：_bulk
        ``` 
            { action: { metadata }}\n
            { request body        }\n
            { action: { metadata }}\n
            { request body        }\n
             ...
        
        
        如： POST /_bulk
            { "delete": { "_index": "website", "_type": "blog", "_id": "123" }} 
            { "create": { "_index": "website", "_type": "blog", "_id": "123" }}
            { "title":    "My first blog post" }
            { "index":  { "_index": "website", "_type": "blog" }}
            { "title":    "My second blog post" }
            { "update": { "_index": "website", "_type": "blog", "_id": "123", "_retry_on_conflict" : 3} }
            { "doc" : {"title" : "My updated blog post"} } 
                               
        ```
      - action/metadata 行指定 哪一个文档做什么操作 。 action为：
        1. create： 如果文档不存在，那么就创建它。
        2. index： 创建一个新文档或者替换一个现有的文档。
        3. update: 部分更新一个文档
        4. delete：删除一个文档 
        
3. 分布式文档存储
    - 路由一个文档到一个分片中： `shard = hash(routing) % number_of_primary_shards`
        - routing 为可变值，默认为文档 `_id` 
    - 主分片和副本分片的交互： 
        - 我们可以发送请求到集群中的任一节点 （协调节点(coordinating node)， 是一种角色，而不是真实的Elasticsearch的节点）。 
        - 每个节点都有能力处理任意请求。每个节点都知道集群中任一文档位置，所以可以直接将请求转发到需要的节点上。
        - 当发送请求的时候， 为了扩展负载，更好的做法是轮询集群中所有的节点。
    - 新建，索引，删除： 都是写操作，必须在主分片完成之后，再复制到相关的副本分片。然后主分片所在节点，向协调节点返回。
    - 检索一个文档
        - 客户端 随机向 node 发请求，假设为 （node1， node1 称之为协调节点）
        - node1 使用文档的 `_id` 确定文档所属分片（假设属于分片0）， node1 将此次请求转发到拥有分片0 的节点上
            （在处理读取请求时，协调结点在每次请求的时候都会通过轮询所有的副本分片来达到负载均衡），假设为node2. 
        - node2 将文档返回给协调节点node1， 然后node1 将文档返回客户端。
    - 更新一个文档
    
4. 搜索 - 最基本的工具
    - 空搜索： 返回集群中所有索引下的所有文档
        - `GET /_search`
        
5. 映射和分析
    - 倒排索引： 词语文档列表
    - 分析与分析器：
        - 分析：  
            - 文本分成适合于倒排索引的独立的 词条 ， 
            - 将这些词条统一化为标准格式以提高它们的“可搜索性”，或者 recall
        - 分析器：三个功能
            - 字符过滤器： 分词前整理字符串， 去掉HTML，或者将 & 转化成 and
            - 分词器： 字符串被 分词器 分为单个的词条
            - Token 过滤器： 改变词条（大写转小写）， 删除词条（停用词），增加词条（同义词）
    - 什么时候适用分析器：当我们 索引 一个文档，它的全文域被分析成词条以用来创建倒排索引。
           - 全文域（string）： 索引和检索，使用相同的分析器
           - 精确域(keyword, date等)： 不会适用
    - 映射 mapping : GET /_mapping 查看
        - 字符串 string text
        - 整数 byte short integer long
        - 浮点型 float double 
        - 布尔 boolean
        - 日期 date
        
6. 请求体查询
    - 空查询： GET /_search {}
    - 查询表达式 DSL  GET /_search   {"query": YOUR_QUERY_HERE}
    - 查询与过滤 
        - 过滤情况（filtering context）： 不评分， 结果只有yes or no
        - 查询情况（query context）: 评分， 代表匹配程度
    - 最重要的查询
        - match_all
        - match
        - multi_match
        - range: 大于gt 大于等于gte 小于lt 小于等于lte
        - term: 查询对于输入的文本不分析, 对给定的值进行精确查询
        - terms
        - exits 和 missing
    - 组合多查询： bool
        - must: 文档 必须 匹配这些条件才能被包含进来
        - must not: 文档 必须不 匹配这些条件才能被包含进来
        - should: 如果满足这些语句中的任意语句，将增加 _score ，否则，无任何影响。它们主要用于修正每个文档的相关性得分。
            - minimum_should_match
        - filter : 必须 匹配，但它以不评分、过滤模式来进行。这些语句对评分没有贡献，只是根据过滤标准来排除或包含文档。
    - 验证查询是否合法：
        - GET /{index}/_validate/query   {查询体}
        - GET /{index}/_validate/query?explain   {查询体}
        
7.  排序与相关性
    - 排序： sort， 如果设置sort ，就不再计算_source。 （如果非要计算score, track_scores 设置为true）
    - 相关性： 
        - fuzzy 查询会计算与关键词的拼写相似程度
        - terms 查询会计算 找到的内容与关键词组成部分匹配的百分比
        - query 查询会计算TF-IDF （相似度算法被定义为检索词频率/反向文档频率， TF/IDF）
            - 检索词频率 ：检索词在该字段出现的频率， 出现频率越高，相关性也越高
            - 反向文档频率： 每个检索词在索引中出现的频率， 出现频率越高，相关性越低
            - 字段长度准则： 字段的长度是多少， 长度越长，相关性越低
            
8. 执行分布式搜索

    两阶段的过程：查询 （query）+ 取回(fetch)  
   ```
    对于： 
        GET /_search
    {
        "from": 90,
        "size": 10
    } 
   ```
    - 查询阶段
         1. 客户端发送请求到协调节点, 协调节点会创建一个大小为 from+size 的空优先队列
         2. 协调节点将请求转发到索引的每个主分片或者副本分片中， 每个分片在本地执行查询，并添加结果到大小为from+size 的本地优先队列
         3. 每个分片返回各自优先队列给协调节点，合并这些值到自己的优先队列中来产生一个全局排序后的结果列表。
         ```
          1. 协调节点广播请求到索引中每一个节点的分片拷贝， 查询请求可以被某个主分片或某个副本分片处理， 所以更多的副本可以增加吞吐量。
          2. 协调节点将在之后的请求中轮询所有的分片拷贝来分摊负载。
          3. 每个分片创建的结果集足够大， 均可以满足全局的搜索请求。
          4. 分片返回一个轻量级的结果列表到协调节点，它仅包含文档 ID 集合以及任何排序需要用到的值，例如 _score 
         ```  
    - 取回阶段
        1. 协调节点辨别出哪些文档需要被取回并向相关的分片提交多个 GET 请求。（multi-get request）
        2. 每个分片加载并 丰富 文档(_source)，如果有需要的话，接着返回文档给协调节点。
        3. 一旦所有的文档都被取回了，协调节点返回结果给客户端。
    - 搜索选项
        - 超时问题timeout： 通常分片处理完它所有的数据后再把结果返回给协同节点，协同节点把收到的所有结果合并为最终结果。
            这意味着花费的时间是最慢分片的处理时间加结果合并的时间。如果有一个节点有问题，就会导致所有的响应缓慢。
            
## 2. 深入搜索
1. 结构化搜索
 - 精确值查找: filter 非评分查询
    - term ： 处理数字（numbers）、布尔值（Booleans）、日期（dates）以及文本（text）
        ```
        GET /{index}/_search
        {
            "term" : {
                "price" : 20
            }
        }
        # 适用filter 转化为非得分查询
        GET /{index}/_search
        {
            "query" : {
                "constant_score" : {         
                    "filter" : {
                        "term" : { 
                            "price" : 20
                        }
                    }
                }
            }
        } 
        ```
      
    
## Elasticsearch分布式一致性原理剖析
  
- [Elasticsearch分布式一致性原理剖析](https://zhuanlan.zhihu.com/p/34858035)
1. ES集群构成 : 节点Node, 
    ```
    conf/elasticsearch.yml:
    node.master: true/false
    node.data: true/false 
    ```
2. 节点发现
   - ZenDiscovery
   ```
   conf/elasticsearch.yml:
   discovery.zen.ping.unicast.hosts: [1.1.1.1, 1.1.1.2, 1.1.1.3] 
   ```
3. Master选举
    - master选举谁发起，什么时候发起？
      - 即当一个节点发现包括自己在内的多数派的master-eligible节点认为集群没有master时，就可以发起master选举。
    - 当需要选举master时，选举谁？
        - 选举的是排序后的第一个MasterCandidate(即master-eligible node)
        - 排序规则：
           - 当clusterStateVersion越大，优先级越高。这是为了保证新Master拥有最新的clusterState(即集群的meta)，避免已经commit的meta变更丢失。因为Master当选后，就会以这个版本的clusterState为基础进行更新
           - 当clusterStateVersion相同时，节点的Id越小，优先级越高。
    - 什么时候选举成功？
       - 得票超过半数则选举成功
    - 怎么保证不脑裂？   
    
4. 错误检测(心跳机制)
    1. MasterFaultDetection与NodesFaultDetection
        - 一类是Master定期检测集群内其他的Node
        - 另一类是集群内其他的Node定期检测当前集群的Master
        
5. 集群扩缩容
    1. 扩容DataNode
        - 配置`conf/elasticsearch.yml`
        ```
        conf/elasticsearch.yml:
        node.master: false
        node.data: true
        ```
       - 配置集群名、节点名等其他配置
        ```
        conf/elasticsearch.yml:
        cluster.name: es-cluster
        node.name: node_Z
        discovery.zen.ping.unicast.hosts: ["x.x.x.x", "x.x.x.y", "x.x.x.z"] 
        ```
