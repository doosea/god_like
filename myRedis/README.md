## redis 
### 1. redis 数据类型
    1. string
        - 增： set key value
        - 查： get key
        - 删： del key
        - 增（多个）： mset key1 value1 key2 value2
        - 查（多个）mget key1 key2
        - 获取字符串长度： strlen key
        - 追加信息到原始信息后部: append key value 
        - 扩展操作
            - incr key  
            - incrby key  
            
    2. list : 双向列表
        - 增: (左右)
            - lpush key value1 [value2]
            - rpush key value1 [value2]
        - 查： 
            - lrange key start stop： 切片查询
            - lindex key index：  获取指定index下的元素
            - llen key： 长度
        - 获取并移除数据：
            - lpop key 
            - rpop key 
        - 扩展操作
            - 规定时间内获取并移除操作
                - blpop key1 [key2] timeout
                - brpop key1 [key2] timeout
            - lrem key count value: 移除指定数据
            
    3. hash
        - 增: hset key field value
        - 查: hget key field
            - hegtall key 
        - 删: del key field1 [field2]
        - 增: hmset key field1 value1 field2 value2
        - 查: hget key field1 field2     
        - 获取哈希表中字段的数量： hlen key  
        - 获取哈希表是否存在指定字段： hexists key field  
        
        - 扩展操作
            - hkeys key: 获取hash表中所有的字段名
            - hvals key: 获取hash表中所有的字段值
            - hincrby key 
        
    4. set
        - 增： sadd key member1 [member2]
        - 查： smembers key
        - 删： srem key member1 [member2]
            
    5. sorted set
        - 增： zadd key score1 member1 [score2 member2]
        - 查： 
            - zrange key start stop [withscores] 
            - zrevrange key start stop [withscores]
        - 删：zrem key member [member ...]
        
### 2. Springboot 整合redis

1. 启动 
    - redis-server：　服务端 
    - redis-cli：客户端
２．Jedis 使用  
    
3. SpringBoot + redis 　
    - [了解 Redis 并在 Spring Boot 项目中使用 Redis](https://developer.ibm.com/zh/articles/know-redis-and-use-it-in-springboot-projects/)
    - [springboot整合redis，推荐整合和使用案例（2021版）](https://blog.csdn.net/yu102655/article/details/112217778)
    - 操作字符串：redisTemplate.opsForValue()
    - 操作 Hash：redisTemplate.opsForHash()
    - 操作 List：redisTemplate.opsForList()
    - 操作 Set：redisTemplate.opsForSet()
    - 操作 ZSet：redisTemplate.opsForZSet()

## Redis 面试题
- [几率大的Redis面试题（含答案）](https://blog.csdn.net/Butterfly_resting/article/details/89668661)
1. redis支持的数据类型
    - String 字符串： set key value, get key 
        - 
    - Hash 哈希 ： hmset name  key1 value1 key2 value2    , hget key filed
        - HashMap
    - List列表：  lpush  name  value，   rpush  name  value, lrange key start end 
        - 双向链表， 增删快
    - Set 集合，sadd key member， smembers key 
        - 哈希表实现，元素不重复， 复杂度 O(1), 共同好友，好友推荐
    - Zset 有序集合 zadd key score member , zrangebyscore key start end
        - zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。每个元素都会关联一个double类型的分数, 通过分数来为集合中的成员进行从小到大的排序
2. 什么是Redis持久化？Redis有哪几种持久化方式？优缺点是什么？    
    - 持久化就是把内存的数据写到磁盘中去，防止服务宕机了内存数据丢失。
    - 两种持久化方式:RDB（默认） 和AOF 
        - RDB (Redis DataBase)： rdbSave-> RDB文件， rdbLoad -> 文件加载内存 
        - AOF (Append-only file): 每次操作都会调用 flushAppendOnlyFile 函数 ，都会执行以下两个操作 （AOF 写入保存）
            - WRITE：根据条件，将 aof_buf 中的缓存写入到 AOF 文件
            - 根据条件，调用 fsync 或 fdatasync 函数，将 AOF 文件保存到磁盘中
    - 比较
        1、aof文件比rdb更新频率高，优先使用aof还原数据。
        2、aof比rdb更安全也更大
        3、rdb性能比aof好
        4、如果两个都配了优先加载AOF
3. redis 通信协议 RESP        
4. Redis 有哪些架构模式？讲讲各自的特点
    - 单机版， 优点： 简单， 缺点： 1、内存容量有限 2、处理能力有限 3、无法高可用。
    - 主从模式（master-slave）, 转移master读数据库的压力， 缺点： 无法保证高可用， 没有解决 master 写的压力
    - 哨兵模式（Redis sentinel）: 分布式系统中监控 redis 主从服务器，并在主服务器下线时自动进行故障转移
        - 监控（Monitoring）,不断地检查你的主服务器和从服务器是否运作正常
        - 提醒（Notification）, 当被监控的某个 Redis 服务器出现问题时， Sentinel 可以通过 API 向管理员或者其他应用程序发送通知。
        - 自动故障迁移（Automatic failover）, 当一个主服务器不能正常工作时， Sentinel 会开始一次自动故障迁移操作
        - 特点： 保证高可用， 监控各个节点， 自动故障迁移， 缺点： 主从模式，切换需要时间丢数据，没有解决 master 写的压力 
    - 集群（proxy 型）
        - 支持失败节点自动删除， 后端 Sharding 分片逻辑对业务透明，业务方的读写方式和操作单个 Redis 一致， 
        - 增加了新的 proxy，需要维护其高可用。
    - 集群（直连型）
        - 无中心架构（不存在哪个节点影响性能瓶颈），少了 proxy 层， 可扩展性， 高可用， 实现故障自动failover
        - 资源隔离性较差，容易出现相互影响的情况, 数据通过异步复制,不保证数据的强一致性
5.  使用过Redis分布式锁么，它是怎么实现的？
           
6. 缓存穿透问题， 如何避免， 什么事缓存雪崩， 如何避免
    - 缓存穿透： 一般的缓存系统，都是按照key去缓存查询，如果不存在对应的value，就应该去后端系统查找（比如DB）。一些恶意的请求会故意查询不存在的key,请求量很大，就会对后端系统造成很大的压力。这就叫做缓存穿透。
    - 缓存穿透的避免： 
        - 布隆过滤器， 对一定不存在的key进行过滤。可以把所有的可能存在的key放到一个大的Bitmap中，查询时通过该bitmap过滤。  
        - 对空结果也进行缓存， 时间设置短一点即可
    - 缓存雪崩： 当缓存服务器重启或者大量缓存集中在某一个时间段失效，这样在失效的时候，会给后端系统带来很大压力。导致系统崩溃
        - 简单地办法，将缓存缓存失效时间分散开，不同的key，设置不同的过期时间，让缓存失效的时间点尽量均匀
        - 系统设计时，在缓存失效后，通过加锁或者队列来控制读数据库写缓存的线程数量。比如对某个key只允许一个线程查询数据和写缓存，其他线程等待
7. 单线程的redis为什么这么快
    - 纯内存操作
    - 单线程操作，避免了频繁的上下文切换
    - 采用了非阻塞I/O多路复用机制