"""
Django settings for burhan project.
"""

import os
from pathlib import Path
from urllib.parse import unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"


def env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def db_from_database_url(url: str):
    parsed = urlparse(url)
    scheme = (parsed.scheme or "").lower()

    if scheme in {"postgres", "postgresql"}:
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": unquote((parsed.path or "").lstrip("/")),
            "USER": unquote(parsed.username or ""),
            "PASSWORD": unquote(parsed.password or ""),
            "HOST": parsed.hostname or "",
            "PORT": str(parsed.port or "5432"),
        }

    if scheme in {"mysql"}:
        return {
            "ENGINE": "django.db.backends.mysql",
            "NAME": unquote((parsed.path or "").lstrip("/")),
            "USER": unquote(parsed.username or ""),
            "PASSWORD": unquote(parsed.password or ""),
            "HOST": parsed.hostname or "",
            "PORT": str(parsed.port or "3306"),
        }

    if scheme in {"sqlite", "sqlite3"}:
        db_path = (parsed.path or "").lstrip("/")
        if not db_path:
            db_path = "db.sqlite3"
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / db_path),
        }

    raise ValueError(f"Unsupported DATABASE_URL scheme: {scheme}")


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-b^g7iz#gz10xgu9_w#n-_tnb#%6(pw&%1od$qp#@z65iakcv#n",
)
DEBUG = env_bool("DJANGO_DEBUG", default=False)

raw_hosts = os.environ.get("ALLOWED_HOSTS", "")
if raw_hosts.strip():
    ALLOWED_HOSTS = [host.strip() for host in raw_hosts.split(",") if host.strip()]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.onrender.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_portal",
    "student_portal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "burhan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "burhan.wsgi.application"
ASGI_APPLICATION = "burhan.asgi.application"

database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {"default": db_from_database_url(database_url)}
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.environ.get("DB_NAME", "school_management"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "12345"),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [FRONTEND_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "student_portal:login"
LOGIN_REDIRECT_URL = "student_portal:dashboard"
LOGOUT_REDIRECT_URL = "student_portal:login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
