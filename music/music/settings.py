"""
Django settings for music project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0b75$cg($hovux9^uwcj!wth+x2t18bn%_id9h*5h873x+v&!2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
# 添加新增的项目应用index、ranking、play、comment、search和user
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
    'ranking',
    'user',
    'play',
    'search',

]
# 添加中间件LocaleMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 使用中文
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music.urls'

# 设置模版路径，在每个App里分别创建模版文件夹templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                  os.path.join(BASE_DIR, 'index/templates'),
                  os.path.join(BASE_DIR, 'ranking/templates'),
                  os.path.join(BASE_DIR, 'user/templates'),
                  os.path.join(BASE_DIR, 'play/templates'),

                  ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'music.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# 设置数据库连接信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'music_db',
        'USER':'root',
        'PASSWORD':'123',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}

SESSION_ENGINE = "redis_sessions.session"
SESSION_REDIS = {
 'host': '127.0.0.1',
    'port': 6379,
 'db': 0,
    'password': '123',
    'prefix': 'session',
    'socket_timeout': 10
}

# redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "123",
        }
    }
}
REDIS_TIMEOUT=7*24*60*60
CUBES_REDIS_TIMEOUT=60*60
NEVER_REDIS_TIMEOUT=365*24*60*60



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_ROOT = './music'
STATIC_URL = '/static/'
# STATICFILES_DIRS用于收集admin的静态资源文件
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.163.com"#去邮箱里去找SMTP服务器地址
EMAIL_PORT = 25
EMAIL_HOST_USER = "mymusicwebsite@163.com"#发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = "ZIKQAYKCWLQNGQTZ"#授权密码
EMAIL_FROM = "我的音乐|验证码"#收件人看到的发件人


SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = 'SAMEORIGIN'
#在settings.py末尾加入
import mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')


