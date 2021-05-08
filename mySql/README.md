# Mysql 优化
0. 基本概念
    - 连接： mysql -u root -p
    - 操作命令
        - show databases; 展示所有的数据库
        - use [database]; 使用指定的数据库
        - show tables;    展示当前书库下的所有表
        - show engines; ：查看支持的引擎
        - show variables like '%storage_engine%'; : 查看当前的存储印引擎
        - 创建表时指定数据库对象的引擎：
            ```sql
            create table tb(
              id int(4) auto_increment,
              name varchar(5),
              department varchar(5),
              primary key(id)
            )ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
            ```
1. Mysql 分层
    - 连接层：提供与客户端的连接 
    - 服务层
        - 提供各种用户适用的接口
        - 提供SQL 优化器 （MYSQL Query Optimizer）
    - 引擎层： 提供了各种存储数据的方式
        - InnoDB： 事务优先， 适合高并发操作： 行锁
        - MyISAM： 性能优先， 表锁
    - 存储层： 存储数据
2. SQL 优化    [步步深入：MySQL架构总览->查询执行流程->SQL解析顺序](https://www.cnblogs.com/annsshadow/p/5037667.html)
    ```sql
    SELECT DISTINCT
    < select_list >
    FROM
        < left_table > < join_type >
    JOIN < right_table > ON < join_condition >
    WHERE
        < where_condition >
    GROUP BY
        < group_by_list >
    HAVING
        < having_condition >
    ORDER BY
        < order_by_condition >
    LIMIT < limit_number >
    ```
    1. SQL 语句
        - 编写过程： select distinct... from... join ... on ...where... group by ... having ... order by ... limit ...
        - 解析过程： from... on ...join ... where... group by ... having ... select distinct... order by ... limit ...
    2. SQL 优化主要是在优化索引

## 索引 index
1. 索引概述
    - 帮助MYSQL 高效获取数据的数据结构
2. 索引优势劣势       
    - 优势
        - 提高检索效率，降低数据库的IO成本
        - 通过索引列对数据排序，降低数据排序成本，降低cpu消耗
    - 劣势
        - 索引数据本身也是一张表，该表中保存了主键与索引字段，并指向实体类的记录，所以索引列也是占用空间的
        - 虽然索引提高查询效率，但是也降低了更新表的速度，如INSERT,UPDATE,DELETE。更新表要维护索引字段
3. 索引结构： MYSQL 在存储引擎层中实现的， 而不是在服务器层实现的
    - BTREE 索引， 最常见的索引类型
    - HASH 索引
    - R-TREE 空间索引
    - Full-text 全文索引
    1. B 树， 又称多路平衡树
        - 性质
            - 树中每个节点最多包含m个孩子
            - 除根节点与叶子节点外，每个节点至少有 [ceil(m/2)] 个孩子, m / 2 向上取整
            - 若跟节点不是叶子节点，则至少有两个孩子
            - 所有的叶子节点在同一层   
            - 每个非叶子节点由n个key和n+1个指针组成，其中 ,[ceil(m/2)-1]<=n<=m-1      
    2. B+ 树
    3. Mysql中的 B+ 树
4. 索引分类
5. 索引语法
6. 索引设计原则