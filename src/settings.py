from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DEBUG = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0"]
LANGUAGE_CODE = "en-us"
MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "media/"
ROOT_URLCONF = "src.urls"
SECRET_KEY = "django-insecure-#ezlo7tqc&h07y4g^1i3jqg78^z*jgsyd11kq812^=k4%!lk6b"
STATIC_ROOT = "/static/"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
TAILWIND_APP_NAME = "theme"
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = "src.wsgi.application"

PORTFOLIO_PROFILE = {
    "NAME": "Bryce Nall",
    "FIRST_NAME": "Bryce",
    "LAST_NAME": "Nall",
    "EMAIL": "btn04@gmail.com",
    "PHONE": None,
    "SOCIALS": {
        "DISCORD": None,
        "YOUTUBE": {
            "display_name": "Bryce Nall",
            "profile_link": "https://www.youtube.com/@brycenall7439/",
            "username": "brycenall7439",
        },
        "INSTAGRAM": {
            "display_name": "bryce nall",
            "profile_link": "https://www.instagram.com/bybnall/",
            "username": "bybnall",
        },
        "FACEBOOK": None,
        "TIKTOK": None,
        "TWITTER": None,
        "REDDIT": None,
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "bucket": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "theme",
    "django_browser_reload",
    "tailwind",
    "django_htmx",
    "crimsonslate_portfolio.apps.CrimsonslatePortfolioConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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
