from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hf=s#xawwi-v(=5^*2be%2_te_9s)7i86hna9(3qp16^=xl=t)'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['mirror','localhost']
INSTALLED_APPS.append('blog')

try:
    from .local import *
except ImportError:
    pass
