import os
from .base import * #noqa
from .base import env

SECRET_KEY= env("DJANGO_SECRET_KEY", default="DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS=["http://localhost:8080"]

ALLOWED_HOSTS = []



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailhog'
EMAIL_PORT = 1025



