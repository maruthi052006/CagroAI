import os

project_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/agri_dt_backend"

apps = [
    "core", "accounts", "data_layer", "agents", "coordination", 
    "simulation", "alerts", "messaging", "api", "zones"
]

def make_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Manage.py
manage_py = """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""
make_file(f"{project_dir}/manage.py", manage_py)

# Config
settings_py = """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-test-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',
    'drf_spectacular',
"""
for app in apps:
    settings_py += f"    'apps.{app}',\n"
settings_py += """]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
"""

make_file(f"{project_dir}/config/__init__.py")
make_file(f"{project_dir}/config/settings.py", settings_py)

urls_py = """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
]
"""
make_file(f"{project_dir}/config/urls.py", urls_py)

# Apps
for app in apps:
    app_dir = f"{project_dir}/apps/{app}"
    make_file(f"{app_dir}/__init__.py")
    make_file(f"{app_dir}/admin.py", "from django.contrib import admin\n")
    make_file(f"{app_dir}/models.py", "from django.db import models\n")
    make_file(f"{app_dir}/views.py", "from django.shortcuts import render\n")
    make_file(f"{app_dir}/tests.py", "from django.test import TestCase\n")
    apps_py = f"""from django.apps import AppConfig

class {app.capitalize().replace('_', '')}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
"""
    make_file(f"{app_dir}/apps.py", apps_py)

# api urls.py
api_urls_py = """from django.urls import path

urlpatterns = [
    # path('predict/', PredictView.as_view()),
]
"""
make_file(f"{project_dir}/apps/api/urls.py", api_urls_py)

print("Django project scaffolded successfully via python.")
