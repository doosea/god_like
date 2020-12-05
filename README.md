# keep learning

## docker
    

[docker_readme](docker/README.md)


## ElasticSearch
[elasticSearch_readme](elasticSearch/README.md)



## linux 
### 权限管理
1. 改变文件所有权（chown）
    ```shell script
    sudo chown username myfile       // 将myfile文件的所有权改为username的
   
    chown -R username /files/work    // 加入-R, work后文件夹以及文件夹里的所有文件和子目录所有权都变为username
    ```
   
2. 改变文件的权限（chmod）
    ```shell script
    sudo chmod 777 filename   //  filename 的权限变为 可读可写可执行
 
    sudo chmod -R 754 director   // director文件夹所有文件的权限变为 可读可写可执行
    ```
   - 三个数字顺序分别代表 用户、用户组、其他 
   - 4 可读, 2 可写, 1可执行, 0无权限
   
3. 用户创建 `useradd`
     - `-g`可以设定用户的主要组
     - `-G`可以设定用户的附加组
     
     ```shell script
     useradd -g 组名 用户名              用户建立时为其创建或指定一个组
     useradd -m 用户名                   创建用户,并为用户建立主目录
     ```