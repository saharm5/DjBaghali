"""
Django settings for DjBaghali project.


For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

import os
from pathlib import Path

# =================== مسیرهای اصلی پروژه ===================
BASE_DIR = Path(__file__).resolve().parent.parent

# =================== امنیت و تنظیمات عمومی ===================
SECRET_KEY = 'django-insecure-wdapy@+a=4x#i!$q5$d#4z%bn+-s40x23dlu&+)3)&zdp4q2vx'

DEBUG = True  # 🚨 در محیط Production مقدار False شود

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# =================== احراز هویت کاربران ===================
AUTH_USER_MODEL = 'authentication.User'

# =================== اپلیکیشن‌های نصب شده ===================
INSTALLED_APPS = [
    "corsheaders",  # حتماً قبل از middleware ثبت شود
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    # اپلیکیشن‌های پروژه
    'authentication',
    'App',
    'AddFavorite',
    'AddCart',
]

# =================== تنظیمات REST FRAMEWORK ===================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# =================== تنظیمات Middleware ===================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ⚠️ حتماً در ابتدای لیست باشد
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =================== تنظیمات مسیرهای اصلی پروژه ===================
ROOT_URLCONF = 'DjBaghali.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'DjBaghali.wsgi.application'

# =================== تنظیمات دیتابیس ===================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# =================== اعتبارسنجی پسورد ===================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =================== تنظیمات زبان و زمان ===================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =================== مدیریت فایل‌های استاتیک ===================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# =================== مقدار پیش‌فرض Auto Field ===================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =================== تنظیمات CORS ===================
CORS_ALLOW_ALL_ORIGINS = True  # 🚨 مقدار True فقط برای تست توصیه می‌شود
#
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://localhost:8080",
#     "http://192.168.110.104:5173",
#     "http://192.168.21.1:5173",
#     "http://192.168.223.1:5173",
#     "http://192.168.111.164:8080",
# ]

CORS_ALLOW_CREDENTIALS = True  # اگر از کوکی‌های احراز هویت استفاده می‌کنید

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS"
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
