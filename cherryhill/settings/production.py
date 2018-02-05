from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

SECRET_KEY = 'hf=s#xawwi-v(=5^*2be%2_te_9s)7i86hna9(3qp16^=xl=t)'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['mirror','localhost','www.lifeinphilly.info','cherryhill-190118.appspot.com']
INSTALLED_APPS.append('blog')

try:
    from .local import *
except ImportError:
    pass

# mysql root password
# BPwdEI3Ij0mqzq9L