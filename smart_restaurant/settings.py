from pathlib import Path
import os
import uuid
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Docker PostgreSQL vars

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER=  os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Render PostgreSQL vars

RENDER_POSTGRES_HOST = os.getenv("RENDER_POSTGRES_HOST")
RENDER_POSTGRES_USER = os.getenv("RENDER_POSTGRES_USER")
RENDER_POSTGRES_PASSWORD = os.getenv("RENDER_POSTGRES_PASSWORD")
RENDER_POSTGRES_PORT = os.getenv("RENDER_POSTGRES_PORT")
RENDER_POSTGRES_DB = os.getenv("RENDER_POSTGRES_DB")

# Device

DEVICE_AUTHENTICATION_TOKEN = uuid.UUID(os.getenv("DEVICE_AUTHENTICATION_TOKEN"))
DEVICE_LOGIN_TOKEN = uuid.UUID(os.getenv("DEVICE_LOGIN_TOKEN"))
DEVICE_RESET_PASSWORD_TOKEN = uuid.UUID(os.getenv("DEVICE_RESET_PASSWORD_TOKEN"))
CREATE_SUPERUSER_TOKEN = uuid.UUID(os.getenv("CREATE_SUPERUSER_TOKEN"))

# Mercado Pago

MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
MP_WEBHOOK_SECRET = os.getenv("MP_WEBHOOK_SECRET")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [".onrender.com"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'devices', 
    'control_panel',
    'restaurant_menu',
    'cart',
    'kitchen',
    'payment'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smart_restaurant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smart_restaurant.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': RENDER_POSTGRES_DB,
        'HOST': RENDER_POSTGRES_HOST,
        'USER': RENDER_POSTGRES_USER,
        'PORT': RENDER_POSTGRES_PORT,
        'PASSWORD': RENDER_POSTGRES_PASSWORD,
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

# DRF

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication"]
}

# User

AUTH_USER_MODEL = 'devices.Device'

# Media

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Secure
SECURE_SSL_REDIRECT = True # Redireciona cliente para requisição https se ele veio de http
SESSION_COOKIE_SECURE = True # Permite que os cookies sejam enviados apenas se a requisição for https
CSRF_COOKIE_SECURE = True # Permite que csrf token seja enviado apenas se a requisição for https
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")