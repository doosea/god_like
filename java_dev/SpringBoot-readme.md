# SpringBoot 
1. 底层注解
    - @SpringBootApplication
         - @SpringBootConfiguration
         - @EnableAutoConfiguration
         - @ComponentScan()
    - @configuration : 代替spring中的xml配置
    - @Import(Class<?> []) : 给容器中自动创建组件， 默认组件名就是犬类名
    - @Conditional (条件装配)
        - @ConditionalOnBean: 有某个bean才装配该bean
        - @ConditionalOnMissingBean : 没有某个bean才装配该bean
        - ...
    - @ImportResource("..xml"), 导入spring 的配置文件
    - @ConfigurationProperties(prefix="前缀")   配置绑定
    - @EnableConfigurationProperties(Obj.class)
2. 自动配置原理
    - @SpringBootApplication
        - @SpringBootConfiguration = Configuration
        - @ComponentScan 指定扫描
        - @EnableAutoConfiguration
            - @AutoConfigurationPackage：
                - 利用Register给容器中导入一些列组件
                - 将指定的一个包下的所有组件导入进来， MainApplication所在包
            - @Import(AutoConfigurationImportSelector.class)
                - 