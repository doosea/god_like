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
  