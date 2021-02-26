# JVM
0. JVM, JRE, JDK 
    - JVM
    - JRE = JVM + 基础类库（java.lang等等）
    - JDK = JVM + 基础类库 + 编译工具

1. JVM 体系结构， 5个部分
    - 类加载器（Class Loader）
    - 运行时数据区（Runtime Data Area）
    - 执行引擎（Execution Engine）
    - 本地库接口（Native Interface）
    - 本地方法库（Native Libraies）
    
 ![jvm结构图](https://ask.qcloudimg.com/http-save/6552462/76d9taggw.jpeg?imageView2/2/w/1620)

2. 运行时数据区， 内存结构
    - PC Register: 程序计数器（Program Counter Register）, 寄存器 PC Register
        - 记住下一条jvm指令的执行地址
        - 线程私有 
        - 唯一一个不会存在内存溢出（OOM: out of memory）的地方
    - 虚拟机栈（JVM Stack）