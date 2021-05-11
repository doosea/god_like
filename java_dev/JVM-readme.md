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
0. class 类的生命周期
    - loading: 加载 （Bootstrap ClassLoader, Extension ClassLoader, App ClassLoader, Customer ClassLoader 双亲委派机制， 安全 and 避免重复加载）
    - linking: 连接 
        - verification: 验证
        - preparation: 准备，半初始化
        - resolution: 解析
    - initialization: 初始化
    - using: 使用
    - unloading: 卸载
        
1. 对象的创建过程： 类初始化(只进行一次) + 实例初始化
    - class loading： 加载对象的字节码文件到内存
    - class linking:
        - verification: 验证是否为 class 字节码文件（前面几位为CAFE BABE）; 等等..
        - preparation: 类的静态变量分类内存，并赋值对应数据类型为默认值（0, 0L, null, false等等）， 同时将常量分配到方法区
        - resolution: 将常量池中的符号引用转化为直接引用
    - initialization: 按照代码书写顺序执行static变量赋值（为变量赋初始值）、static代码块。
    - 申请对象内存
    - 成员变量赋值，对应类型的默认值
    - 调用构造方法
        - 1. 成员变量顺序赋初始值
        - 2. 执行构造方法语句
2. 对象在内存中存储布局
    - 普通对象, T t = new T();
        - 对象头 : markword(8个字节)
        - classPointer, 指向T.class， （-XX:+UserCompressedClassPointer 占4个字节，否则不开启为8个字节）
        - InstanceData:
            - 1. 引用类型， 实例数据， （-XX:UserCompressedOops，占4字节， 否则不开启8字节， Ordinary Object Pointers）
        - padding: 使得对象所占所有字节之和可以被8整除
    - 数组对象
        - 对象头 : markword(8个字节)
        - classPointer, 指向T.class， （-XX:+UserCompressedClassPointer 占4个字节，否则不开启为8个字节）
        - 数组长度: 4字节
        - 数组数据
        - padding: 8 倍数  
3. 对象头具体包括什么, 不同的状态，对应的markword也不同（无锁，轻量级锁，重量级锁，偏向锁）
    - 锁标记
    - hashcode
    - GC age年龄（4位，最大15）
    
4. 一个对象占用多少个字节
    - Object o = new Object()  : 16 = 8(markword) + 4(classPointer) + 0(instanceData) + 4(Padding)
5. 对象定位
    - 句柄池, GC时，效率较高
    - 直接指针（hotspot）
    
6. JVM RUNTime Data Area and JVM instructions
    1. PC 程序计数器

    JVM 执行过程    
    while not end:
        取pc中的位置；
        找到对应位置的指令；
        执行该指令；
        PC++;

## Soul
### HashMap
- [HashMap 一遍就懂！！！！](https://blog.csdn.net/qq_40574571/article/details/97612100)
- [史上最全HashMap面试题汇总](https://blog.csdn.net/QGhurt/article/details/107323702)
1. java.util.Map 接口
    - HashMap: 非线程安全
    - HashTable： 承自Dictionary类，并且是线程安全， 任意时间只有一个线程能够写HashTable, 并发性不如ConcurrentHashMap
    - LinkedHashMap: LinkedHashMap是HashMap的一个子类
    - TreeMap: TreeMap实现SortedMap接口，能够把它保存的记录根据键排序，默认是按键值的升序排序
2. HashMap 存储结构: HashMap是数组+链表+红黑树(JDK1.8增加了红黑树部分)
    - HashMap就是使用哈希表来存储的, 哈希冲突解决方法： 开放地址法和链地址法（java）
    - 哈希桶数组 Node[] table 初始化长度16， （2的n次方， 合数）， Load Factor = 0.75， threshold = length * load Factor, size超过threshold 就会扩容， 两倍，
        modCount记录HashMap内部结构变化发生的次数
    - 当链表长度太长（默认超过8）时， 
    
3. 根据key获取哈希桶数组索引位置： (h ^ (h >>> 16)) & (length -1)
    - 取哈希值： h= key.hashCode()
    - 高位运算： h ^ (h >>> 16)
    - 取模运算： h & (length-1)
    -  a % b == (b-1) & a ,当b是2的指数时，等式成立。
    
    
4. put()的详细执行
    - 当前哈数桶数组是否为null, 否则resize()
    - key 的hash值计算数组索引下标i, 如果数组对应元素null,创建新节点直接插入，否则    
    - 判断首个元素是否相同， 是覆盖， 否则
    - 判断是否是treeNode, 即是否是红黑树， 是红黑树，直接利用红黑树插入键值对， 否则
    - 遍历table[i], 判断列表长度是否大于8， 大于8转化红黑树，在红黑树中执行插入操作，否则链表插入， 遍历过程中，如果相同，覆盖
    - 插入成功后， size++ 与阈值threshold比较，超过则扩容
    
5. 扩容过程resize()
    - 创建一个新的数组,其容量为旧数组的两倍,并重新计算旧数组中结点的存储位置。结点在新数组中的位置只有两种,原下标位置或原下标+旧数组的大小
        - HashMap在进行扩容时，使用的rehash方式非常巧妙，因为每次扩容都是翻倍，与原来计算的 (n-1)&hash的结果相比，只是多了一个bit位，所以结点要么就在原来的位置，要么就被分配到"原位置+旧容量"这个位置。
    - 链表的对象个数如果达到了8个，此时如果数组长度没有达到64，那么HashMap会先扩容解决，如果已经达到了64，那么这个链表会变成红黑树，结点类型由Node变成TreeNode类型

6. ConcurrentHashMap : 线程安全的HashMap
    -  ConcurrentHashMap 底层数据结构: 数组+链表/红黑二叉树
    -  实现线程安全的方式（重要)
        - 在JDK1.7的时候，ConcurrentHashMap（分段锁）, segment, 每一把锁只锁容器其中一部分数据
        - JDK1.8 的时候已经摒弃了Segment的概念, 并发控制使用 synchronized 和 CAS 来操作
7. 红黑树
    1. 5个原则
        - 每个结点要么是红的要么是黑的。  
        - 根结点是黑的。  
        - 每个叶结点（叶结点即指树尾端NIL指针或NULL结点）都是黑的。  
        - 如果一个结点是红的，那么它的两个儿子都是黑的。  
        - 对于任意结点而言，其到叶结点树尾端NIL指针的每条路径都包含相同数目的黑结点
    2. 左旋
        
    3. 右旋
- 利用红黑树快速增删改查的特点提高HashMap的性能 http://blog.csdn.net/v_july_v/article/details/6105630
-  CAS 自旋锁


## JVM
1. .java -> .Class 文件 -> Class Loader -> 运行时数据区（）
2.  运行时数据区, 栈和pc不会垃圾回收
    - 方法区 : Method area， 线程共享， 方法区常量池
        - 静态变量static, 常量 final, 类信息class（构造方法，接口定义），运行时的常量池
    - Java 栈: Stack, 栈帧
    - 本地方法栈: Native Method Stack
    - 堆: Heap
        - Eden 区
        - 
    - 程序计数器： PC， 线程私有
3. Native 关键字： native 说明本地调用不到了，调用底层C语言的库；
    - 会进入本地方法栈，调用本地方法接口JNI Java Native interface, 扩展java的使用
## JVM - 黑马程序员笔记
- [黑马程序员JVM完整教程](https://www.bilibili.com/video/BV1yE411Z7AP?p=7)
- [JVM 学习笔记](https://blog.csdn.net/weixin_50280576/article/details/113742011)
### 1. 概述
    - ClassLoader：Java 代码编译成二进制后，会经过类加载器，这样才能加载到 JVM 中运行。
    - Method Area：类是放在方法区中。
    - Heap：类的实例对象。
    - 当类调用方法时，会用到 JVM Stack、PC Register、本地方法栈。
    - 方法执行时的每行代码是有执行引擎中的解释器逐行执行，方法中的热点代码频繁调用的方法，由 JIT 编译器优化后执行，GC 会对堆中不用的对象进行回收。需要和操作系统打交道就需要使用到本地方法接口。
### 2. 内存结构
1. 运行时数据区
    - PC Register 程序计数器 （线程私有）
    - JVM Stacks JVM虚拟机栈  （线程私有）
    - Native Method Stacks 本地方法栈 （线程私有）
    - Method Area 方法区  （线程共享）
    - Heap 堆  （线程共享）
2. 程序计数器  
    - 是记录下一条 jvm 指令的执行地址行号。
    - 线程私有， 不会内存溢出
3.  虚拟机栈 
    - 每个线程运行需要的内存空间，称为虚拟机栈
    - 每个栈由多个栈帧（Frame）组成，对应着每次调用方法时所占用的内存 
    - 每个线程只能有一个活动栈帧，对应着当前正在执行的方法
    - 垃圾回收不会设计栈内存， 方法调用结束后，弹出栈
    - 方法内的局部变量是否线程安全
        - 如果方法内部的变量没有逃离方法的作用访问，它是线程安全的
        - 如果是局部变量引用了对象，并逃离了方法的访问，那就要考虑线程安全问题, (入参， 出参)
    - 栈内存溢出： java.lang.stackOverflowError
        - 栈帧过多， 
        - JVM 参数，使用-Xss256k 指定栈内存大小
    - 线程诊断
        - 定位进程号，top：  命令查看cpu使用情况，可以定位到线程
        - 定位线程号， ps H -eo pid,tid,%cpu|grep pid-number
        - jstack 进程 id， 通过查看进程中的线程的 nid ，刚才通过 ps 命令看到的 tid 来对比定位，
           注意 jstack 查找出的线程 id 是 16 进制的，需要转换。
4. 本地方法栈 native   
    - 一些带有 native 关键字的方法就是需要 JAVA 去调用本地的C或者C++方法，因为 JAVA 有时候没法直接和操作系统底层交互，
       所以需要用到本地方法栈，服务于带 native 关键字的方法。
5. 堆 
    - 通过new关键字创建的对象都会被放在堆内存
    - 它是线程共享，堆内存中的对象都需要考虑线程安全问题
    - 垃圾回收机制
    - 堆内存溢出 java.lang.OutofMemoryError ：java heap space. 
        - JVM 参数， 可以使用 -Xmx8m 来指定堆内存大小
    - 堆内存诊断
        - jps： 查看前系统中有哪些 java 进程         
        - jmap：查看堆内存占用情况， jmap - heap 进程id 
        - jconsole： 图形界面的，多功能的监测工具，可以连续监测
        - jvisualvm： 图形界面， 功能更强大
6. 方法区
    - 存储 类信息和运行时常量池
    - 方法区域在逻辑上是堆的一部分， 不同 JVM有不同的实现方式
        - Hotspot JVM JDK1.6版本 使用永久代PermGen来实现
        - Hotspot JVM JDK1.8版本以后 使用元空间Metaspace， 使用本地内存（操作系统内存）
            - 但是 StringTable 是放在堆中的， 不是放在元空间中
    - 方法区溢出   
        -  1.8 之前会导致永久代内存溢出  java.lang.OutOfMemoryError: PermGen space
            - 使用 -XX:MaxPermSize=8m 指定永久代内存大小
        -  1.8 之后会导致元空间内存溢出 java.lang.OutOfMemoryError: Metaspace
            - 使用 -XX:MaxMetaspaceSize=8m 指定元空间大小
7. 运行时常量池 
    - 二进制字节码包含（类的基本信息，常量池，类方法定义，包含了虚拟机的指令）
    - javap -v Test.class 命令反编译查看结果
    - 常量池 Constant Pool, 就是一张表，虚拟机指令根据这张常量表找到要执行的类名、方法名、参数类型、字面量信息
    - 运行时常量池: 常量池是 *.class 文件中的，当该类被加载以后，它的常量池信息就会放入运行时常量池，并把里面的符号地址变为真实地址
8. StringTable ["a", "b", "ab"], hashtable 结构
    - 常量池中的字符串仅是符号，只有在被用到时才会转化为对象
    - 利用串池的机制，来避免重复创建字符串对象
    - 字符串变量拼接的原理是StringBuilder
    - 字符串常量拼接的原理是编译器优化
    - 可以使用intern方法，主动将串池中还没有的字符串对象放入串池中
    - jdk1.6 StringTable 位置是在永久代中，1.8 StringTable 位置是在堆中。
    - StringTable 垃圾回收 
        - -Xmx10m 指定堆内存大小
        - -XX:+PrintStringTableStatistics 打印字符串常量池信息
        - -XX:+PrintGCDetails
        - -verbose:gc 打印 gc 的次数，耗费时间等信息
        - -XX:StringTableSize=桶个数（最少设置为 1009 以上）
   ```java
    public static void main(String[] args) {
		String s1 = "a";
		String s2 = "b";
		String s3 = "ab";
		String s4 = s1 + s2;    // new StringBuilder().append("a").append("b").toString()  == new String("ab")
        String s5 = "a" + "b"   // javac编译期间的优化， JVM层面直接转化为 "ab", 在常量池检查，如没有则创建"ab"
   
        // s3 在常量池中， s4 new出来的在堆中，所以地址不同， false 
        System.out.println(s3 == s4);  //false
   
        System.out.println(s3 == s5);  //true
	}

   ```
9. 直接内存Direct Memory
    - 常见于 NIO 操作时，用于数据缓冲区
    - 分配回收成本较高，但读写性能高
    - 不受 JVM 内存回收管理
    - java 不能直接操作文件管理，需要切换到内核态,使用本地方法进行操作，然后读取磁盘文件，会在系统内存中创建一个缓冲区，将数据读到系统缓冲区，
        然后在将系统缓冲区数据，复制到 java 堆内存中(缓冲区)。缺点是数据存储了两份，在系统内存中有一份，java 堆中有一份，造成了不必要的复制。
    -  DirectBuffer 文件读取流程： 直接内存是操作系统和 Java 代码都可以访问的一块区域，无需将代码从系统内存复制到 Java 堆内存，从而提高了效率。
    - 直接内存的垃圾回收： java.lang.OutOfMemoryError:Direct buffer Memory
        - 直接内存的回收不是通过 JVM 的垃圾回收来释放的
        - unsafe.freeMemory 手动释放直接内存
        - 使用了 Unsafe 类来完成直接内存的分配回收，回收需要主动调用freeMemory 方法      
        - ByteBuffer 的实现内部使用了 Cleaner（虚引用）来检测 ByteBuffer 。一旦ByteBuffer 被垃圾回收，那么会由 
            ReferenceHandler（守护线程） 来调用 Cleaner 的 clean 方法调用 freeMemory 来释放内存
        - -XX:+DisableExplicitGC  // 禁止显示的 GC， 即 程序中的System.gc()
### 3. 垃圾回收
1. 如何判断对象可以回收
    1. 引用计数法
        - python 采取引用计数的方式， 缺点容易造成循环引用
    2. 可达性分析（根可达法）
        - JVM 中的垃圾回收器通过可达性分析来探索所有存活的对象
        - 扫描堆中的对象，看能否沿着 GC Root 对象为起点的引用链找到该对象，如果找不到，则表示可以回收
        - 可以作为 GC Root 的对象
            - 虚拟机栈（栈帧中的本地变量表）中引用的对象
            - 方法区中类静态属性引用的对象
            - 方法区中常量引用的对象
            - 本地方法栈中 JNI（即一般说的Native方法）引用的对象
    3. 四种引用（五种引用）
        - 强引用 (StrongReference)
            - 只有所有 GC Roots 对象都不通过【强引用】引用该对象，该对象才能被垃圾回收
        - 软引用（SoftReference）
            - 仅有软引用引用该对象时，在垃圾回收后，内存仍不足时会再次出发垃圾回收，回收软引用对象
            - 可以配合引用队列来释放软引用自身
        - 弱引用（WeakReference）
            - 仅有弱引用引用该对象时，在垃圾回收时，无论内存是否充足，都会回收弱引用对象
            - 可以配合引用队列来释放弱引用自身  
        - 虚引用（PhantomReference）
            - 必须配合引用队列使用，主要配合 ByteBuffer 使用，被引用对象回收时，会将虚引用入队，
                由 Reference Handler 线程调用虚引用相关方法释放直接内存
        - 终结器引用（FinalReference）
            - 无需手动编码，但其内部配合引用队列使用，在垃圾回收时，终结器引用入队（被引用对象暂时没有被回收），
                再由 Finalizer 线程通过终结器引用找到被引用对象并调用它的 finalize 方法，第二次 GC 时才能回收被引用对象。
2. 垃圾回收算法
    1. 标记清除 Mark Sweep
        - 速度快， 会产生内存碎片
    2. 标记整理 Mark Compact
        - 速度慢，没有内存碎片
    3. 复制 Copy 
        - 不会产生内存碎片， 需要占用两倍的内存空间
3. 分代垃圾回收(新生代minor gc ，老年代)
    - 新创建的对象首先分配在eden区 （eden:survive form : survive to = 8:1:1）
    - 新生代空间不足时，触发 minor gc ，eden 区 和 from 区存活的对象使用 - copy 复制到 to 中，存活的对象年龄加一，然后交换 from to
    - minor gc 会引发 stop the world，暂停其他线程，等垃圾回收结束后，恢复用户线程运行
    - 当幸存区对象的寿命超过阈值时，会晋升到老年代，最大的寿命是 15（4bit）
    - 当老年代空间不足时，会先触发 minor gc，如果空间仍然不足，那么就触发 full fc ，停止的时间更长！
    - 相关的JVM参数
        - 堆初始大小	-Xms
        - 堆最大大小	-Xmx 或 -XX:MaxHeapSize=size
        - 新生代大小	-Xmn 或 (-XX:NewSize=size + -XX:MaxNewSize=size )
        - 幸存区比例（动态）	-XX:InitialSurvivorRatio=ratio 和 -XX:+UseAdaptiveSizePolicy
        - 幸存区比例	-XX:SurvivorRatio=ratio
        - 晋升阈值	-XX:MaxTenuringThreshold=threshold
        - 晋升详情	-XX:+PrintTenuringDistribution
        - GC详情	-XX:+PrintGCDetails -verbose:gc
        - FullGC 前 MinorGC	-XX:+ScavengeBeforeFullGC

4. 垃圾回收器
    0. 概念
        - 并行收集：指多条垃圾收集线程并行工作，但此时用户线程仍处于等待状态。
        - 并发收集：指用户线程与垃圾收集线程同时工作（不一定是并行的可能会交替执行）。用户程序在继续运行，而垃圾收集程序运行在另一个 CPU 上
        - 吞吐量：即 CPU 用于运行用户代码的时间与 CPU 总消耗时间的比值（吞吐量 = 运行用户代码时间 / ( 运行用户代码时间 + 垃圾收集时间 )），
            也就是。例如：虚拟机共运行 100 分钟，垃圾收集器花掉 1 分钟，那么吞吐量就是 99% 。
    1. 串行
        - 单线程， 堆内存较少，适合个人电脑
        - -XX:+UserSerialGC = Serial + SerialOld 
            - Serial minor GC, 使用的复制算法， SerialOld 老年代GC 使用的是标记整理算法
            - 
    2. 吞吐量优先
        - 多线程
        - 堆内存较大，多核 cpu
        - 让单位时间内，STW 的时间最短 0.2 0.2 = 0.4
    3. 响应时间优先
        - 多线程
        - 堆内存较大，多核 cpu
        - 尽可能让 STW 的单次时间最短 0.1 0.1 0.1 0.1 0.1 = 0.5
    - 
5. 垃圾回收调优
6. 案例 
   - 案例1：Full GC 和 Minor GC 频繁
   - 案例2：请求高峰期发生 Full GC，单次暂停时间特别长（CMS）
   - 案例3：老年代充裕情况下，发生 Full GC（jdk1.7）                  
### 4. 类加载与字节码技术&内存模型