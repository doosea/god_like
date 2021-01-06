# Personal Recommendation Algorithm  学习笔记

## 1. 综述
### 1.1 个性化推荐算法综述

课程大纲：
1. Recall 召回
    - FM
    - Graph-based
    - Content-based
    - Graph-embed
    - Item2Vec
2. Rank 排序
    - LR
    - GBDT
    - LR + GBDT
    - DNN 
3. Evaluate
    1. offline
        - AUC
        - Precise
        - Recall
        - RE Recom
        - Re Rank
    2. online
        - CTR
        - ViewTime
        - TotalRecomID
4. 环境
   - python, tensorflow, word2vec, xgboost

### 1.2 个性化召回算法综述

1. 个性化召回： 从item全集中选取一部分作为候选集
2. 个性化召回算法
    - 基于用户行为的
    - 基于 user profile 的
    - 基于隐语义的
3. 工业界个性化召回框架
   pass

## 2. LFM(latent factor model)

### 2.1 LFM 综述
1. LFM 算法： 
    根据 User Item 的矩阵 P, 求出user 和item 的向量表示
    
### 2.2 LFM 理论知识与公式推导

![LFM损失函数推导](../sourceFile/pic/recommendation_1.jpg)
- P（u, i）: 代表用户 user 对 item 的关系矩阵（喜欢/点击为1， 否则为0, 或者是评分。）
- F ：user 和item 的向量维度， 隐特征个数 (10-32)
- 正则项系数 a （0.01-0.05）
- 学习率 b （0.01-0.05）

### 2.3 LFM code 实现
1. 数据集
    - recommendation/data/movies.txt
    - recommendation/data/ratings.txt
    
2. code
    - recommendation/LFM

## 3 Personal Rnak 
> [参考连接](https://blog.csdn.net/thormas1996/article/details/89479779)
1. 概念： 图， 顶点， 边， 二分图
2. 图中顶点的相关度主要取决与以下因素： 
    - 两个顶点之间路径数 
    - 两个顶点之间路径长度 
    - 两个顶点之间路径经过的顶点
    
3. 而相关性高的顶点一般有如下特性： 
    - 两个顶点有很多路径相连 
    - 连接两个顶点之间的路径长度比较短 
    - 连接两个顶点之间的路径不会经过出度较大的顶点
    
4. 迭代形式公式 
![s](../sourceFile/pic/recommendation_2.jpg)
    - in(v) 表示 指向 v 的节点的集合
    - out(v) 表示 v 指向的节点的结合, |out(v)|出度
    - vA 表示初始点，  
    ```
      其中 PR(A) = （1-alpha）*(len(out(A))) + alpha*()
                = 3*(a-alpha) + 1/2 * alpha * rank[a] +  1/2 * alpha * rank[b] + 1/2 * alpha * rank[d]
    ```
5. Personal Rank 矩阵形式
![s](../sourceFile/pic/recommendation_3.jpg)     
    - r: （m+n）* 1 的列向量， m user 个数， n item 个数
    - r0: 除了被推荐的user 对应的行值为1， 其余为0
    - M: 表示转移概率矩阵，顶点之间有连接边的为，出度的倒数， 否则为0
    

## 4. item2Vec
