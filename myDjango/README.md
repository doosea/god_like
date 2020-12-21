# django 框架的学习

## django框架

1. 命令行模式：
    - `pip install django`
    - `django-admin startproject 项目名称(django_demo)`: 创建django项目
    - `cd django_demo` 切换到项目根目录
    - `python manage.py startapp 应用名(myApp_demo)` : 创建app应用

2. 目录结构
     ```text
    .
    ├── django_demo
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── myApp_demo
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── README.md
    └── templates
    ```       
3. WSGI概念(Web Server Gateway Interface)
    - Web服务器网关接口:Web服务器和Python应用程序之间交互的一种规范
    - Web服务器：` server`或`gateway` 和 应用程序端 `application`或者 `framework`   
  
  
## django 后端项目链接mysql

### 1. 项目构建
- `django-admin startproject search_hot`: 创建django项目`search_hot`
- `debug_man.py` 参数： `runserver`
- `django-admin startapp search_hot_web`: 添加django app
- `python manage.py runserver [ip:port]`: 启动django服务

- `python manage.py makemigrations`: 
- `python manage.py migrate`: 
- `python manage.py shell`: 进入shell 


1. `from django.urls import include, path` 中的 `path`参数解析：
    - route(必须):  一个匹配 URL 的准则（类似正则表达式）
    - view(必须): route 对应的视图函数， 传入一个 `HttpRequest` 对象作为第一参数
    - kwargs(可选): dict
    - name(可选):  URL 取名能使你在 Django 的任意地方唯一地引用它

2. 数据库配置
    - 修改 `seetings.py` 中的 `DATABASES`
        ```python
           DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'HOST': MYSQL_HOST,
                'NAME': NAME,
                'USER': USER,
                'PASSWORD': PASSWORD,
                'PORT': PORT,
                # 初始化 mysql 设置， 编码格式
                'OPTIONS': {
                    'init_command': 'SET default_storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci;'}
            }
           }
        ```
   
3. 引入 django restful framework: 
    - [django-rest-framework.org](https://www.django-rest-framework.org/tutorial/quickstart/)
    - `pip install djangorestframework`
    - `Project seetings.py` 中 `INSTALLED_APPS` 添加
        ```python
        INSTALLED_APPS = [
            ...
            'rest_framework',
        ]
        ```
    - App 下 `models.py` 定义自己的model, 生成数据库
        - `python manage.py makemigrations`
        - `python manage.py migrate`
        - `python manage.py shell`
            ```python
              # 写入数据
              Movie.objects.create(name="test_movie1", description="des_1.........")
              # 查询所有数据
              Movie.objects.all()
            ```
          
    - App下生成`serializers.py`, 创建model 对应的 `Modelserializers` 对象
        ```python
        from rest_framework import serializers
        from .models import Movie
        
        
        class MovieSerializer(serializers.HyperlinkedModelSerializer):
            class Meta:
                model = Movie
                fields = "__all__"
        ```
      
    - App 下的 `Views.py` 创建对应的 `modelViewSet`
        ```python
        from rest_framework import viewsets
        from django.http import HttpResponse
        from .models import Movie
        from .serializers import MovieSerializer
        
        
        class MovieViewSet(viewsets.ModelViewSet):
            """
               API endpoint that allows users to be viewed or edited.
            """
            queryset = Movie.objects.all()
            serializer_class = MovieSerializer
        ```
    - `Project urls.py` 添加 router:
        ```python
        from django.contrib import admin
        from django.urls import path, include
        from rest_framework import routers
        from search_hot_web import views
        
        router = routers.DefaultRouter()
        router.register(r'movie', views.MovieViewSet)
        
        urlpatterns = [
            # 注册router 到总路由
            path('api/', include(router.urls)),
        
            path('admin/', admin.site.urls),
            path('h1/', include("search_hot_web.urls")),
        ]
        ```
    
    - 总结： 
        1. `Project settings.py `中注册 `rest_framework` 和 `search_hot_web`
        2. `App models.py` 创建`Model`类
        3. `App serializers.py` 创建 `Model` 对应的 `ModelSerializer` 类
        4. `App views.py` 创建 `Model` 对应的 `ModelViewSet` 类
        5. `Project urls.py` 添加 `router`, 注册 `router` 到总路由
        6. 访问`http://127.0.0.1:8000/api/movie/`

4. 解决django 跨域问题: 
    - [参考连接](https://www.cnblogs.com/daviddd/p/12051522.html)
    - `pip install django-cors-headers`     
    - 添加到setting的app中
        ```python
        INSTALLED_APPS = (
            ...
            'corsheaders',
            ...
        )
        ```
    - 添加中间件
        ```python
        MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
            ...
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            ...
        ]
        ```
    - setting下面添加下面的配置
        ```python
        CORS_ORIGIN_ALLOW_ALL = True
        ```
      


### django连接本地es crud
注意事项：
1. 本地docker 开启es 和 kibana
   ``` 
    docker run --name es -p 9200:9200 -p 9300:9300 \
         -e ES_JAVA_OPTS="-Xms64m -Xmx128m" \
         -e "discovery.type=single-node" \
         -v /mydata/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
         -v /mydata/elasticsearch/data:/usr/share/elasticsearch/data \
         -v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
         -d elasticsearch:7.4.2 
         
    docker run --name kibana -e ELASTICSEARCH_HOSTS=http://192.168.0.107:9200 -p 5601:5601 -d kibana:7.4.2
    ``` 
2. python 下与elasticsearch 交互的客户端
    - [参考连接](https://blog.csdn.net/wujiandao/article/details/81607107)
    - elasticsearch-py
    - elasticsearch-dsl
 
3. 使用drf-haystack连接
  
4. 使用python elasticsearch 操作
    - [python-elasticsearch基本用法](https://www.cnblogs.com/mrzhao520/archive/2004/01/13/14120991.html)
    - 
    
5. 复合查询
- A and B
    ```text
        GET blog/_search
        {
          "query":{
            "bool": {
              "must": [
                {
                  "match_phrase": {
                    "title": "创新"
                  }
                },{
                  "match_phrase": {
                    "title": "科技"
                  }
                }
              ]
            }
          }
        }
    ```

- A 0r B 
    ```text
        GET blog/_search
        {
          "query": {
            "bool": {
              "should": [
                {
                  "match_phrase": {
                    "content": "创新"
                  }
                },
                {
                  "match_phrase": {
                    "content": "科技"
                  }
                }
              ],
              "minimum_should_match": 1
            }
          }
        }
    ```

- A and (B or C)
    ```text
        GET blog/_search
        {
          "query": {
            "bool": {
              "must": [
                {
                  "match_phrase": {
                    "title": "创新"
                  }
                },{
                  "match_phrase": {
                    "title": "科技"
                  }
                }
              ],
              "should": [
                {
                  "match_phrase": {
                    "content": "创新"
                  }
                },
                {
                  "match_phrase": {
                    "content": "科技"
                  }
                }
              ],
              "minimum_should_match": 1
            }
          }
        }
    ```