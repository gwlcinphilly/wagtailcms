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
'''


DATABASES = {

    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME': 'home',
        'USER': 'root',
        'PASSWORD' : 'BPwdEI3Ij0mqzq9L',
        'PORT' : '3306'
        }
}
DATABASES['default']['HOST'] = '/cloudsql/cherryhill-190118:us-central1:home'

if os.getenv('GAE_INSTANCE'):
    pass
else:
    DATABASES['default']['HOST'] = '127.0.0.1'
'''