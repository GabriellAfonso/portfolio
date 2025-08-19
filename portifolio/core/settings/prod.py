from .base import *
import os
from dotenv import load_dotenv
dotenv_path = BASE_DIR / "dotenv_files/.env.prod"
load_dotenv(dotenv_path)


SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')

DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',')
    if h.strip()
]

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'change-me'),
        'NAME': os.getenv('POSTGRES_DB', 'change-me'),
        'USER': os.getenv('POSTGRES_USER', 'change-me'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'change-me'),
        'HOST': os.getenv('POSTGRES_HOST', 'change-me'),
        'PORT': os.getenv('POSTGRES_PORT', 'change-me'),
    }
}


TEMPLATE_DEBUG = False
CORS_ALLOW_ALL_ORIGINS = False
CSRF_TRUSTED_ORIGINS = [os.getenv('SITE_URL', 'change-me')]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
