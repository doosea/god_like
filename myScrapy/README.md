# 爬虫学习笔记

- [python分布式爬虫打造搜索引擎--------scrapy实现](https://www.cnblogs.com/jinxiao-pu/p/6706319.html)
- [参考连接](https://blog.csdn.net/qq_23079443/article/details/73920584?utm_source=copy)

## 聚焦爬虫
1. 聚焦爬虫:爬取页面中指定的页面内容。
    - 编码流程：
        - 指定url
        - 发起请求
        - 获取响应数据
        - 数据解析
        - 持久化存储

2. 数据解析分类：
    - 正则
    - bs4
    - xpath（***）

3. 数据解析原理概述：
    - 解析的局部的文本内容都会在标签之间或者标签对应的属性中进行存储
    - 1.进行指定标签的定位
    - 2.标签或者标签对应的属性中存储的数据值进行提取（解析）

4. bs4进行数据解析
    - bs4数据解析的原理：
        - 1.实例化一个BeautifulSoup对象，并且将页面源码数据加载到该对象中
        - 2.通过调用BeautifulSoup对象中相关的属性或者方法进行标签定位和数据提取
    - 环境安装：
        - pip install bs4
        - pip install lxml
    - 如何实例化BeautifulSoup对象：
        - from bs4 import BeautifulSoup
        - 对象的实例化：
            - 1.将本地的html文档中的数据加载到该对象中
                 - fp = open('./test.html','r',encoding='utf-8')
                 - soup = BeautifulSoup(fp,'lxml')
            - 2.将互联网上获取的页面源码加载到该对象中
                - page_text = response.text
                - soup = BeatifulSoup(page_text,'lxml')
        - 提供的用于数据解析的方法和属性：
            - soup.tagName:返回的是文档中第一次出现的tagName对应的标签
            - soup.find():
                - find('tagName'):等同于soup.div
                - 属性定位：
                    -soup.find('div',class_/id/attr='song')
            - soup.find_all('tagName'):返回符合要求的所有标签（列表）
        - select：
            - select('某种选择器（id，class，标签...选择器）'),返回的是一个列表。
            - 层级选择器：
                - soup.select('.tang > ul > li > a')：>表示的是一个层级
                - oup.select('.tang > ul a')：空格表示的多个层级
        - 获取标签之间的文本数据：
            - soup.a.text/string/get_text()
            - text/get_text():可以获取某一个标签中所有的文本内容
            - string：只可以获取该标签下面直系的文本内容
        - 获取标签中属性值：
            - soup.a['href']

5. xpath解析：最常用且最便捷高效的一种解析方式。通用性。
    - xpath解析原理：
        - 1.实例化一个etree的对象，且需要将被解析的页面源码数据加载到该对象中。
        - 2.调用etree对象中的xpath方法结合着xpath表达式实现标签的定位和内容的捕获。
    - 环境的安装：
        - pip install lxml
    - 如何实例化一个etree对象:from lxml import etree
        - 1.将本地的html文档中的源码数据加载到etree对象中：
           - etree.parse(filePath)
        - 2.可以将从互联网上获取的源码数据加载到该对象中
           - etree.HTML('page_text')
        - xpath('xpath表达式')
    - xpath表达式:
        - /:表示的是从根节点开始定位。表示的是一个层级。
        - //:表示的是多个层级。可以表示从任意位置开始定位。
        - 属性定位：//div[@class='song'] tag[@attrName="attrValue"]
        - 索引定位：//div[@class="song"]/p[3] 索引是从1开始的。
        - 取文本：
            - /text() 获取的是标签中直系的文本内容
            - //text() 标签中非直系的文本内容（所有的文本内容）
        - 取属性：
            /@attrName     ==>img/src

6. 高性能异步爬虫

    - 目的：在爬虫中使用异步实现高性能的数据爬取操作。

    - 异步爬虫的方式：
        - 1.多线程，多进程（不建议）：
            好处：可以为相关阻塞的操作单独开启线程或者进程，阻塞操作就可以异步执行。
            弊端：无法无限制的开启多线程或者多进程。
        - 2.线程池、进程池（适当的使用）：
            好处：我们可以降低系统对进程或者线程创建和销毁的一个频率，从而很好的降低系统的开销。
            弊端：池中线程或进程的数量是有上限。
    
    - 单线程+异步协程（推荐）：
        - event_loop：事件循环，相当于一个无限循环，我们可以把一些函数注册到这个事件循环上，
        当满足某些条件的时候，函数就会被循环执行。
    
        - coroutine：协程对象，我们可以将协程对象注册到事件循环中，它会被事件循环调用。
        我们可以使用 async 关键字来定义一个方法，这个方法在调用时不会立即被执行，而是返回
        一个协程对象。
    
        - task：任务，它是对协程对象的进一步封装，包含了任务的各个状态。
    
        - future：代表将来执行或还没有执行的任务，实际上和 task 没有本质区别。
    
        - async 定义一个协程.
    
        - await 用来挂起阻塞方法的执行。

# Python分布式爬虫课程Scrapy打造搜索引擎 学习笔记

## 正则表达式

1. 特殊字符
     - ^ ： 以什么开头
     - $ ： 以什么结尾
     - . ： 表示任意字符
     - * ： 前面出现的子表达式0次或者多次
    
>待补充


## 深度优先与广度优先
> mytest|深度优先与广度优先.py

## 字符串编码
1. 概念：
    - Bit: 位 或者 比特， 计算机运算的基础，属于二进制的范畴；
    - Byte : 字节, 1 Byte = 8 Bits,即 1B = 8b
    - KB: 1024 Byte
    - 1 TB = 1024 GB = 1024 * 1024 MB = 1024**3 KB = 1024**4 B = 1024**5 bits
    - 一般用bit作为传输时的单位， 应用层byte

2. 编码方式
    - ASCII : 单字节编码(8 bits)， 一共128个
    - ISO-8859-1： 单字节编码(8 bits)， 扩展ASCII 编码，一共能表示256个字符
    - GB2312： 双字节编码(16 bits)，编码范围是 A1-F7，  A1-A9 是符号区，总共包含 682 个符号，从 B0-F7 是汉字区，包含 6763 个汉字。
    - GBK： 双字节编码(16 bits)，编码范围是 8140~FEFE， 扩展并兼容GB2312，也就是 GB2312 编码的汉字可以用 GBK 来解码，并且不会有乱码。
    - utf-8: 以 8 位为一个编码单位的可变长编码, 会将一个码位编码为 1 到 4 个字节。 
        ```text
          1 个字节：U+ 0000 ~ U+ 007F       0XXXXXXX
          2 个字节：U+ 0080 ~ U+ 07FF       110XXXXX  10XXXXXX
          3 个字节：U+ 0800 ~ U+ FFFF       1110XXXX  10XXXXXX 10XXXXXX
          4 个字节：U+ 10000 ~ U+ 10FFFF    11110XXX  10XXXXXX 10XXXXXX  10XXXXXX
        ```
    - utf-16: 2字节编码或者4字节编码(16 / 32 bits)
    - utf-32: 4字节编码(32 bits)
    
    ```
   ps: 
        Unicode 是编码字符集， 为每一个「字符」分配一个唯一的 ID（学名为码位 / 码点 / Code Point）
        utf-8, utf-16, utf-32... 是编码规范,将「码位」转换为字节序列的规则（编码/解码 可以理解为 加密/解密 的过程）
    ```  
3.  文件读取到存储，解码和编码的整个过程： (通过 Unicode 编码来进行不同编码之间的相互转化)
    - 读取文件： 指定文件的解码规则， encode= ""
    - 修改文件之后
    - 存储文件： 指定文件的编码规则，decode= ""

## 爬虫去重策略
1. 访问过的url存入数据库
2. url==> set中， 只需要o(1)代价查询，但是耗内存
3. url 经过md5等方法哈希后保存到set中（相比前两种，很省内存了）
4. bitmap, 减少内存，但是增加冲突
5. bloomfilter方法对bitmap改进，进行多重hash降低冲突

## scrapy 框架
1. scrapy 框架命令
    - scrapy startproject projectName: 创建scrapy爬虫项目
    - scrapy genspider spiderdemo spiderdemo.com : 创建爬虫模板
    - scarpy crawl spiderdemo: 启动scrapy 爬虫项目
    
2. scrapy 项目架构：
    ```
        ├── ArticleSpider
        │   ├── __init__.py
        │   ├── items.py
        │   ├── middlewares.py
        │   ├── pipelines.py
        │   ├── settings.py
        │   └── spiders
        │       └── __init__.py
        └── scrapy.cfg
    ```

3. 启动scrapy, 创建 debug_main.py
    ```python
        import os
        os.path.abspath(__file__) # 获取当面py文件的绝对路径
        os.path.dirname(os.path.abspath(__file__)) # 获取当前文件的父目录
        
        import sys
        # 
        sys.path.append(os.path.dirname(os.path.abspath(__file__)) ) 
        
        from scrapy.cmdline import execute
        execute(["scrapy", "crawl", "jobbole"])
    ```
   
4. 问题
    - UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb5 in position 251: invalid start byte
        - 检查源网页的编码方式，使用对应的编码方式解码
        
    
    


