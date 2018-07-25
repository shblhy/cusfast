
cusfast
===================


- 项目介绍


    基于django和restframework的开发模板，旨在提高开发效率。
    使用方法：
    下载代码，将项目名全局替换成你需要的项目名。
    更新settings DATABASES 或者写一份自己的 settings_local.py(见最后）
    执行migrate应用表到数据库，执行createsuperuser创建管理员。
    你可以从cauth模块中找到多种常见功能的写法，拷贝到你需要的位置去。
    然后专注于你的开发吧~~


- 重新自行建立项目的一些命令：


1. project

    django-admin.py startproject  abmanagement
    django-admin.py startapp cauth

2. requirements.txt

    pymysql
    Django
    django-cors-headers
    django-filter
    djangorestframework
    jsonfield
    django-smtp-ssl
    django-rest-swagger
    docutils

    pip install -r requirements.txt
    # -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com

3. settings初步配置


    LANGUAGE_CODE = 'en-us'	->	LANGUAGE_CODE = 'zh-cn' 或zh_Hans 与django.conf.locale下一致,注意编码unicode与翻译str的转化
    TIME_ZONE = 'UTC'	->	TIME_ZONE = 'Asia/Shanghai'
    try:
        from .settings_local import *
    except:
        pass


    自定义模块: INSTALLED_APPS

    'django.contrib.admindocs',
    'rest_framework',
    'django_filters',
    ‘rest_framework_swagger’
    'corsheaders',
    'cauth',

4. cauth 为例创建模块

    django-admin.py startapp cauth
    settings
        AUTH_USER_MODEL = "cauth.User"
    tests 测试
    admin 注册到django admin
    apps 注册包
    filters 过滤器
    serializers 序列器
    views 试图
    urls
    utils 常用方法
    exlib 扩展库

5. 数据库 CREATE SCHEMA `qktest_demo` DEFAULT CHARACTER SET utf8 ;

    # python3不支持mysqldb 在主模块__init__.py里加这两句
    import pymysql
    pymysql.install_as_MySQLdb()
    python manage.py makemigrations cauth
    python manage.py migrate
    python manage.py createsuperuser
    启动程序 查看

6. 其它settings配置

    email

    EMAIL_HOST = 'smtp.qq.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = '111111111'
    EMAIL_HOST_PASSWORD = 'kqhwhfqotxwdbdga'
    DEFAULT_FROM_EMAIL = 'huangyan@innotech'
    EMAIL_SUBJECT_PREFIX = '[huangyan]'
    EMAIL_USE_LOCALTIME = True
    EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

7. tests
	# import os;os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cusfast.settings");import django;django.setup()
	右键点方法，Nosetests测试
	Nosetests cauth.tests 测试
	python manage.py test cauth

8. Git 配置和gitignore

    自行复制.gitignore文件

9. settings_local.py


ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1'
)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cusfast',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8',
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}