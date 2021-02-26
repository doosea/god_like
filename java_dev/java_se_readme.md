# JAVA SE
1. JRE JDK JVM 
    - JRE: JAVA runtime environment, java 程序运行时的环境， 包含JVM和运行时所需要的核心类库
    - JDK: java development kit 
    - JVM: java virtual machine 
    - jdk 包含 JRE, JRE 包含 JVM
2. 开发流程
    - 编写.java
    - 编译 .java  == > .class 字节码文件
    - JVM运行
    
3. java 关键字
    - 访问权限： public private protected default(缺省) 
    - 类接口方法变量代码块修饰符：
        - class abstract extends implements interface final static synchronized volatile native enum
    ![](https://pic4.zhimg.com/v2-c0c00df9f72082beba5ce919db4c8d57_r.jpg)

4. 数据类型
    - 基础数据类型：4类8种
        - 整数型： byte short int long
        - 浮点型: float double
        - 字符型: char
        - 布尔型: boolean
    - 引用数据类型
        - 数组 
            - 动态初始化： 数据类型[] 数组名称 = new 数据类型[数组长度];
            - 静态初始化： 数据类型[] 数组名称 = new 数据类型[]{数组数据};
            - 静态初始化（省略）： 数据类型[] 数组名称 = {数组数据};
            
5. 方法
    - 方法的修饰符
        - public static   
    - 方法的重载 overload
    
6. java 内存 
    - 栈内存（stack） : 存放的是方法的局部变量。 方法运行一定要在栈当中运行 
    - 堆内存（heap）： 凡是new 出来的都在堆中
        - 都有16进制地址值
    - 方法区（Method Area）： 存储.class 相关信息，包含方法的信息
    - 本地方法栈（Native Method Stack）： 与操作系统相关
    - 寄存器（pc Register） ： 与CPU相关
    
7. 类
    - 封装， 继承， 多态
    - 标准的类叫做Java Bean 
        - 所有成员变量 private 关键字修饰, 私有化， 本类内部随便使用，外部使用setter,getter 
        - 每个成员变量编写一对儿Getter / Setter
        - 无参构造 和 有参构造
    - static 修饰成员变量， 静态变量，  类名称.方法（）调用
    - static 修饰成员， 静态方法， 类名称.方法（）调用
    
8. 集合
    - 数组 []， 固定长度， 无法改变长度  String[] arr = new String[] 
    - ArrayList 集合， 可变长度： ArrayList<String> list = new ArrayList<>(); 
        - list.add(), list.get() , list.remove(), list.size()

9. 继承， 
    - super 访问父类内容
    - this 访问本类内容