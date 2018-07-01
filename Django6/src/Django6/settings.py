"""
Django settings for Django6 project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.urls.base import reverse_lazy
from django.conf.global_settings import AUTHENTICATION_BACKENDS,\
    LOGIN_REDIRECT_URL, MEDIA_URL, MEDIA_ROOT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#장고에서 제공하는 로그아웃기능을 사용한 뒤 돌아올 페이지 설정
#reverse() : 해당 함수를 호출했을 때 즉시 urls 파일을 탐색해 url 주소를 찾음
#reverse_lazy() : 해당 함수를 호출했을 때 웹서버 실행이 준비되면 urls 파일을 탐색해 url 주소를 찾음
LOGOUT_REDIRECT_URL = reverse_lazy('vote:index')

#로그인이 요구되는 기능을 비로그인상태로 접근할때 로그인할수 있는 페이지 설정
LOGIN_URL = reverse_lazy('customlogin:signin')
#로그인 뷰로 로그인에 성공했을때, 이동할 URL 경로
LOGIN_REDIRECT_URL = reverse_lazy('vote:index')

#구글 개발자 사이트에서 발급받은 키와 비밀번호
#클라이언트 id
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '408287861714-go7f2jqrd92rfbn82f5bg853c8p7j41f.apps.googleusercontent.com'
#클라이언트 보안비밀
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='h1XZt0I0ls1zXghZMw3wAIO9'

AUTHENTICATION_BACKENDS=(
    #구글 인증
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    #구글 로그인과 프로젝트의 Uesr 모델클래스와 매칭할때 사용
    'django.contrib.auth.backends.ModelBackend',
    )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yq+7*v!d!j_re7ms_0ddr3g+%izza-ghvhn&(h(3!lfmsmx+d3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vote',
    'customlogin',
    'social_django', #소셜로그인에 대한 어플리케이션
    'Blog',
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

ROOT_URLCONF = 'Django6.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR], #어떤 폴더에 HTML 파일을 저장할지 설정
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Django6.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

#파이썬 코드에서 파일을 접근할 때의 루트 경로
MEDIA_URL = '/uploads/'
#파일이 실제로 저장되는 경로
#BASE_DIR : 프로젝트가 생성된 위치
#os.path.join(경로, 경로) : 두 폴더 경로를 붙여줌
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')



