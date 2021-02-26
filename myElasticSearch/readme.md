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
5. 各种query
    - match_all: 匹配所有
    - match: 匹配filed包含文本, 会对filed进行分词操作，然后再查询
    - multi match: 和match类似，使用多个filed匹配
    - match_phrase: 短语匹配查询
    - range: range 范围查询，可以放在query或filter里面，在query里面会对相关度分数产生影响
    - term: 完全匹配，也就是精确查询，搜索前不会再对搜索词进行分词拆解。
    - terms: 同term,指定多个搜索词
    - exist: field不能为空(null)
    - wildcard:允许使用通配符　
    - fuzzy： 实现模糊查询,  term 查询的模糊等价, 不会分词
6. DSL 
    - query: 查询
    - sort ： 排序
    - hightlight: 高亮
    - aggs: 
        - 度量聚合：min、max、sum、avg聚合
        - 桶聚合
            - 1、term聚合：词条的聚合， terms聚合为字段中每个词条返回一个桶。

7.     
    