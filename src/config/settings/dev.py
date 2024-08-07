import os
import socket  # only if you haven't already imported this

from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

SWAGGER_SETTINGS = {
    'VALIDATOR_URLS': [
        'http://localhost:8000/__debug__/',  # Agregue la ruta a la barra de herramientas de depuración aquí
    ],
}

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS += ['debug_toolbar']


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
