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
        -e ES_JAVA_OPTS="-Xms64m -Xmx128m" \
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
    
        docker run --name kibana -e ELASTICSEARCH_HOSTS=http://192.168.0.107:9200 -p 5601:5601 -d kibana:7.4.2
        docker run --name kibana -e ELASTICSEARCH_HOSTS=http://10.4.93.246:9200 -p 5601:5601 -d kibana:7.4.2
        踩坑日记：
            - 设置ELASTICSEARCH_HOSTS时， 不应该设置成`localhost`,应该设置成宿主机的ip地址。

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