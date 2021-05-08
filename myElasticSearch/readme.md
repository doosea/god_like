# ES  --  中华石杉
参考连接： [中华石杉-es 基础篇](https://www.bilibili.com/video/BV1p4411h7sR?p=2&spm_id_from=pageDriver)

## 启动 es
```     
首次启动容器
docker run --name es -p 9200:9200 -p 9300:9300 \
    -e ES_JAVA_OPTS="-Xms1g -Xmx1g" \
    -e "discovery.type=single-node" \
    -v /mydata/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
    -v /mydata/elasticsearch/data:/usr/share/elasticsearch/data \
    -v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
    -d elasticsearch:7.4.2 

docker run --name kibanaENN -e ELASTICSEARCH_HOSTS=http://10.4.93.246:9200 -p 5601:5601 -d kibana:7.4.2 

第二次再启动
sudo docker start es 
sudo docker start kibana 
```
   

## 基础篇
1. ElasticSearch 功能： 分布式， 检索， 分析
    - 分布式的数据搜索引擎 和 数据分析引擎
    - 全文检索， 结构化检索， 数据分析
    - 对海量数据进行近实时的处理
2. ES 核心概念
    - 近实时     
    - es集群 ， Node节点 
    - 文档 document
    - 索引， index 和 type 
    - 分片 shard， 建立索引时， 一次设置， 不能再次修改， 默认一个index ： 5 shard (1 replica), 一共十个
    - 副本 replica： 高可用性， 提高吞吐量
    
3. 快速入门案例实战：电商网站商品管理
    1. 简单的集群管理
        - (1)快速检查集群健康: yellow , green , red 
            - GET /_cat/health?v
            - GET /_cat/health
            - GET /_cluster/health
        - (2) 快速查看集群索引
            - GET /_cat/indices?v
        - (3)快速创建索引
            - PUT /index
    2. 文档CRUD
        - 增 ： PUT /{index}/_doc/{id}  {json_data}
        - 查 : GET /{index}/_doc/{id}
        - 更新: POST /{index}/_update/{id}  {"doc":{"name":"jiaqiangban dosea"}}
        - 删除: DELETE /{index}/_doc/{id}
        
4. 多种搜索方式
    1. query string search 
        - 搜索全部商品： 
            - GET /{index}/_search (推荐)    
            - GET /{index}/_doc/_search（废弃）    
        - GET /{index}/_search?q=name:yagao&sort  (一般不用)
    2. query DSL
    3. query filter
    4. full-text search 全文检索： 会将输出的搜索串分词，然后去倒排索引里意义匹配， 只要能匹配上任何一个分词，就可以命中
        - 索引字段，会先分词， 建立倒排索引。
    5. phrase search 
        - 与全文检索相反， 输入的搜索串， 必须和phrase 完全一致 才能命中 
    6. highlight search 
5. DSL 
    - from :
    - size :
    - _source: 
    - query: 查询
        - match_all: 匹配所有
        - match: 匹配filed包含文本, 会对filed进行分词操作，然后再查
        - multi match: 和match类似，使用多个filed匹配
        - match_phrase: 短语匹配查询
        - range: range 范围查询，可以放在query或filter里面，在
        - term: 完全匹配，也就是精确查询，搜索前不会再对搜索词进行分词拆解。
        - terms: 同term,指定多个搜索词
        - exist: field不能为空(null)
        - wildcard:允许使用通配符　
        - fuzzy： 实现模糊查询,  term 查询的模糊等价, 不会分词
    - sort ： 排序
    - hightlight: 高亮
    - aggs: 
        - 度量聚合：min、max、sum、avg聚合
        - 桶聚合
            - 1、term聚合：词条的聚合， terms聚合为字段中每个词条返回一个桶。

## 进阶篇 （IT 论坛 ） 
1. filter 执行原理
    - 倒排索引中，找出 doc list
    - 根据doc list, 构建bitset或者叫bitmap  ([0,1,0,0,0,1]), 用来表示一个doc是否匹配其中的filter条件， 匹配1， 不匹配0
    - 遍历每个filter 条件对应的bitset, 优先最稀疏的，查询出所有满足条件的doc
    - 缓存： caching bitset ， 跟踪最近256个query 中超过一定次数的过滤条件，进行缓存。 对于小segment(<1000, 或者<3% )不缓存bitset
    - filter 会在query 之前执行
        - query 会计算doc对搜索条件的得分，还会根据这个score去排序
        - filter 简单过滤出满足条件的doc, 不给算 relevance score ， 也不排序
    - 如果有doc 被修改或者新增， caching bitset 会被自动更新

2.  多shard 场景下， 搜索结果得分 relevance score 可能不准
    - 主要原因是， idf 的计算是在 local shard 中计算
    - _score  = 搜索词差分之后各个term的得分相加求和
    - 每一个term的得分：score = boost * idf * tf
        - boost
        - idf = log(1 + (N - n + 0.5) / (n + 0.5)
            - n, number of documents containing term
            - N, total number of documents with field 
        - tf = freq / (freq + k1 * (1 - b + b * dl / avgdl))
            - freq, occurrences of term within document
            - k1, term saturation parameter
            - b, length normalization parameter
            - dl, length of field
            - avgdl, average length of field
    - 解决办法： 
        - 生产环境下， 数据量大的时候根据 id路由规则，负载均衡， 数据分布均匀
        - 测试环境下， primary shard = 1 (number_of_shards = 1)
        - 测试环境下， 搜索是附带search_type = dfs_query_then_fetch， 会将local IDF 取回计算global IDF, 生产环境下不推荐，性能很差
3.  best_fields 策略 ： dis_max ,直接取多个query 中得分最高的那个query分数即可   
        - tie_breaker参数
        - boost 
4. multi-match 
    - minimum_should_match 去长尾， 最小匹配个数
    - bese_fields 策略： 将某一个field匹配尽可能多的关键词的doc 返回
    - most_fields 策略： 尽可能返回更多field 匹配到某个关键词的doc， 优先返回回来