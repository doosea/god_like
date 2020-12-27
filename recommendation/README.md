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
数据集： 
    - recommendation/data/movies.txt
    - recommendation/data/ratings.txt
