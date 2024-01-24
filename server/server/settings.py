from pathlib import Path
import configparser

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
config = configparser.ConfigParser()
config.read('config.ini')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('App', 'django_secret')
DEBUG = False

# Application definition
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600

ALLOWED_HOSTS = ['southwest.al3xbro.me']
CORS_ALLOWED_ORIGINS = [
    "southwest.al3xbro.me",
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'corsheaders',
    'reservations.apps.ReservationsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.get('Database', 'database_name'),
        'USER': config.get('Database', 'database_user'),
        'PASSWORD': config.get('Database', 'database_password'),
        'HOST': config.get('Database', 'database_host'),
        'PORT': config.get('Database', 'database_port'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = config.get('App', 'timezone')
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
