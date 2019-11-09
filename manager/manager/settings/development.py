import logging.config
from .base import *  # NOQA


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]["OPTIONS"].update({"debug": True})

# Less strict password authentication and validation
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = []

# Django Debug Toolbar
INSTALLED_APPS += ("debug_toolbar",)


# Additional middleware introduced by debug toolbar
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Show emails to console in DEBUG mode
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True

# Allow internal IPs for debugging
INTERNAL_IPS = ["127.0.0.1"]

LOGFILE_ROOT = BASE_DIR.parent / "logs"
if not os.path.exists(LOGFILE_ROOT):
    os.mkdir(LOGFILE_ROOT)

LOGGING_CONFIG = None
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(LOGFILE_ROOT / "django.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        # "django": {
        #     "handlers": ["default"],
        #     "propagate": True,
        #     "level": "DEBUG",
        # },
        "default": {"handlers": ["default"], "level": "DEBUG"}
    },
}

logging.config.dictConfig(LOGGING)
