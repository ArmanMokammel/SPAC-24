"""
Django settings for insb_spac24 project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('SETTINGS') == 'dev':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'emails',
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

ROOT_URLCONF = 'insb_spac24.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'insb_spac24.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if(os.environ.get('SETTINGS')=='dev'):

    # Sqlite3 in Development
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if(os.environ.get('SETTINGS')=='prod'):
    DATABASES = {
        
        # MySQL in Production
        'default': {
            
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': os.environ.get('PROD_DATABASE_NAME'),
            'USER': os.environ.get('PROD_DATABASE_USER'),
            'PASSWORD': os.environ.get('PROD_DATABASE_PASSWORD'),
            'HOST': os.environ.get('PROD_DATABASE_HOST'),
            'PORT': '3306',
            
        }
        
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
#static directory
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT= os.path.join(BASE_DIR, 'Participant Files/')
MEDIA_URL = "/media_files/"
LOGIN_URL = '/'


GOOGLE_CLOUD_CLIENT_ID=os.environ.get('DEV_GOOGLE_CLOUD_CLIENT_ID')
GOOGLE_CLOUD_PROJECT_ID=os.environ.get('DEV_GOOGLE_CLOUD_PROJECT_ID')
GOOGLE_CLOUD_AUTH_URI=os.environ.get('DEV_GOOGLE_CLOUD_AUTH_URI')
GOOGLE_CLOUD_TOKEN_URI=os.environ.get('DEV_GOOGLE_CLOUD_TOKEN_URI')
GOOGLE_CLOUD_AUTH_PROVIDER_x509_cert_url=os.environ.get('DEV_GOOGLE_CLOUD_AUTH_PROVIDER_x509_cert_url')
GOOGLE_CLOUD_CLIENT_SECRET=os.environ.get('DEV_GOOGLE_CLOUD_CLIENT_SECRET')
SCOPES=os.environ.get('DEV_SCOPES').split(',')

GOOGLE_MAIL_API_NAME=os.environ.get('GOOGLE_MAIL_API_NAME')
GOOGLE_MAIL_API_VERSION=os.environ.get('GOOGLE_MAIL_API_VERSION')

GOOGLE_CLOUD_TOKEN=os.environ.get('GOOGLE_CLOUD_TOKEN')
GOOGLE_CLOUD_REFRESH_TOKEN=os.environ.get('GOOGLE_CLOUD_REFRESH_TOKEN')
GOOGLE_CLOUD_EXPIRY=os.environ.get('GOOGLE_CLOUD_EXPIRY')