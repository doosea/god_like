"""设计一个装饰器，使api请求资源时会读取缓存，并且可以设置缓存的超时时间"""
import time
from datetime import datetime

from flask import Flask

app = Flask(__name__)
created = 0
cache_response = None


def cache(timeout=5):
    """缓存请求的资源，默认缓存失效时间为5秒"""

    def decorator(func):
        def wrapper(*arg, **kwargs):
            global created, cache_response
            now = time.time()
            if now - created > timeout:
                created = now
                cache_response = func(*arg, **kwargs)

            return cache_response

        return wrapper

    return decorator


def cache2(func, timeout=5):
    def wrapper(*arg, **kwargs):
        global created, cache_response
        now = time.time()
        if now - created > timeout:
            created = now
            cache_response = func(*arg, **kwargs)

        return cache_response

    return wrapper


# 添加header的装饰器
def set_header(headers):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            response.headers.update(headers)
            return response

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


@app.route('/')
@cache2(15)
def index():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " > Hello! "


if __name__ == '__main__':
    app.run(debug=True)
