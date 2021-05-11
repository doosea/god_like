# Spring 学习笔记

## 1. Spring 概念
1. Spring 是一个轻量级开源JavaEE 框架
2. 两个核心：
    - IOC： 控制反转, 把创建对象的过程交给spring进行管理
    - AOP： 面向切面，不修改源代码进行功能增强
  
## 2. IOC 容器， inversion of control
1. IOC 底层原理
    - xml 解析
    - 工厂模式
    - 反射
    
2. IOC 接口 (BeanFactory)
    - BeanFactory
    - ApplicationContext

3. IOC 操作Bean管理
    - 创建对象
    - 注入属性
        - set方法注入： property属性
        - 有参构造注入： constructor-arg属性  
    - bean 作用域： 单实例（默认）singleton 或者多实例prototype
    - bean 生命周期  
        -  (1) 通过构造器创建bean实例（无参构造）
        -  (2) 为bean的属性设置值和对其他bean的引用，调用set方法
        -  (3) bean实例传递bean后置处理器的方法 （BeanPostProcessor - postProcessBeforeInitialization）
        -  (4) bean初始化方法（需要配置初始化的方法 init-method）
        -  (5) bean实例传递bean后置处理器的方法 （BeanPostProcessor - postProcessAfterInitialization）
        -  (6) 得到bean对象，可以使用
        -  (7) bean销毁方法（需要配置销毁方法 init-method）
         
4. IOC 操作Bean管理（基于xml）

    
5. IOC 操作Bean管理（基于注解）
    - bean 创建对象 注解, 功能一样，对应不同层
        - @Component
        - @Controller
        - @Service
        - @Repository 
    - bean 属性注入 注解
        - @AutoWired, 根据属性类型自动注入
        - @Qualifier， 根据属性名称自动注入， 须配合AutoWired 一起使用
        - @Resource， 可根据类型或者名称进行注入
        - @Value, 普通属性注入
    - @Configuration ，替代xml 配置文件    
    - @ComponentScan(basePackage={"包的路径"})    
     
## 3. AOP
1. 面向切面编程, 不改变源代码的基础上，进行代码增强， 类似于装饰器
    - AOP 底层使用动态代理， 两种动态代理形式
        - 有接口情况， JDK 动态代理
            - 创建当前类对应接口的实现类代理对象
        - 无接口情况， CGLIB 动态代理
            - 创建当前类的子类的代理对象
    - newProxyInstance
        - ClassLoader loader: 类加载器
        - 类<?>[] interfaces ： 增强方法所在的类
        - InvocationHandler h ： 实现这个接口，创建代理对象，写增强的方法
    - AOP 相关术语
        - 连接点： 类里面有哪些方法可以增强， 这些方法被称为连接点
        - 切入点： 实际被真正增强的方法，称为切入点
        - 通知（增强）： 实际增强的逻辑部分称之为通知（增强）， 
            - 通知有多种类型
                - 前置通知
                - 后置通知
                - 环绕通知
                - 异常通知
                - 最终通知
        - 切面： 动作， 把通知应用到切入点的过程称为切面
    - AspectJ
    - 切入点表达式
        execution(权限修饰符， 返回类型， 类全路径， 方法名称， 参数列表)
    
## 4.JBDC Template

## 5. 事务管理
1. 事务的四个特性
    - 原子性
    - 一致性
    - 隔离性
    - 持久性
    
## 6. spring5.x 新特性