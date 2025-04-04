"""
Django settings for deepBack project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
import boto3
from botocore.client import Config

os.getenv("")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_DOMAIN = os.getenv("SITE_DOMAIN")
SITE_NAME = os.getenv("SITE_NAME")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_SECRET_KEY = os.getenv("GOOGLE_SECRET_KEY")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
PORT = os.getenv("PORT")

MAIL_PRO = os.getenv("MAIL_PRO")

SOUND_CRYPT = os.getenv("SOUND_CRYPT")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

FRONTEND_URL = os.getenv("FRONTEND_URL")

s3_client = boto3.client(
    "s3",
    endpoint_url=AWS_S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
    region_name=AWS_S3_REGION_NAME,
)


STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("BACKEND_PYTHON_SECRET_KEY")
ALGORITHM = os.getenv("BACKEND_ALGORITHM")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # os.getenv("IN_PROD", "False") != "True"

IN_PROD = os.getenv("IN_PROD", "False") == "True"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ["*"]  # En prod remplace par domaines autorisés

CORS_ORIGIN_ALLOW_ALL = not IN_PROD
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = (
    [
        "http://localhost:4200",
        os.getenv("FRONTEND_URL"),
    ]
    if IN_PROD
    else []
)
# PROD

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",
    os.getenv("FRONTEND_URL"),
]
# CSRF_COOKIE_SAMESITE = 'Lax'

# Adaptation des paramètres de sécurité en fonction de l'environnement
if IN_PROD:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    COOKIE_SAMESITE = "None"
    SECURE_SSL_REDIRECT = True
else:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    COOKIE_SAMESITE = "Lax"
    SECURE_SSL_REDIRECT = False


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Remplacez par l'URL de votre serveur Redis
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 'PASSWORD': 'votre_mot_de_passe',  # Si Redis nécessite une authentification
        },
    }
}

# Optionnel : Utiliser le cache comme session backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "app",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    "django_filters",
    "silk",
    "rest_framework_simplejwt",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.twitter",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "silk.middleware.SilkyMiddleware",
    "app.middleware.JWTAuthMiddleware",
]

ROOT_URLCONF = "deepBack.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "deepBack.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", ""),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "app.authentication.SafeJWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "DeepAudio",
    "DESCRIPTION": "Le beau swagger",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# Oauth2 JWT params
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": ALGORITHM,
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_COOKIE": "access_token",  # Nom du cookie JWT d'accès
    "AUTH_COOKIE_REFRESH": "refresh_token",  # Nom du cookie JWT de rafraîchissement
    "AUTH_COOKIE_SAMESITE": "Lax",
    "AUTH_COOKIE_HTTP_ONLY": True,
}

SITE_ID = 1
AUTH_USER_MODEL = "app.User"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# django-allauth configurations
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
LOGIN_REDIRECT_URL = f"{FRONTEND_URL}/"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_GET = True

SOCIAL_AUTH_GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_SECRET_KEY")
SOCIAL_AUTH_TWITTER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
SOCIAL_AUTH_TWITTER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

CACHE_TTL = int(os.environ.get("CACHE_TTL"))

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv("REDIS_PASSWORD"),
        },
    }
}


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
    },
    "twitter": {
        "SCOPE": ["email"],
        "METHOD": "oauth1",
    },
}

FRONTEND_URL = os.getenv("FRONTEND_URL")


STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Limite maximale des données dans la requête (en octets)
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200  # 200 Mo

# Limite maximale de taille de fichier uploadé (en octets)
FILE_UPLOAD_MAX_MEMORY_SIZE = 209715200  # 200 Mo

# Periode d'essai abonnement premium
TRIAL_SUB_PERIOD_DAY = 7

FREE_TOKENS = int(os.getenv("FREE_TOKENS"))

# Mailing system
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
