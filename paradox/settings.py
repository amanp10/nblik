"""
Django settings for paradox project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+aw6*!!(qmu4o!wfu0dfbq2*4v4k^!&o9414yh58*i7$+ik28q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nblik',
    'registration',
    'bootstrap_toolkit',
    'social.apps.django_app.default',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'storages',
)

AUTHENTICATION_BACKENDS = (
  'social_auth.backends.google.GoogleOAuth2Backend',
  'social_auth.backends.contrib.github.GithubBackend',
  'django.contrib.auth.backends.ModelBackend',
  'social_auth.backends.facebook.FacebookBackend',
  'social.backends.twitter.TwitterOAuth',
  'social_auth.backends.contrib.linkedin.LinkedinBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'paradox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_auth.context_processors.social_auth_by_type_backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

#TEMPLATE_PATH=os.path.join(BASE_DIR, 'templates')
#TEMPLATE_DIRS=(TEMPLATE_PATH,)
WSGI_APPLICATION = 'paradox.wsgi.application'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

if 'DEBUG' in os.environ:
    if (os.environ['DEBUG']=='FALSE'):
        DEBUG = False
    else:
        DEBUG = True


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = 'staticfiles'
#STATIC_URL = '/static/'
STATIC_PATH = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = (
    STATIC_PATH,
)
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
#MEDIA_URL='/media/'
MEDIA_ROOT = os.path.join(STATIC_PATH,'media')
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'nitingera1996@gmail.com'
#EMAIL_HOST_PASSWORD = 'geranitin18091996'
#ACCOUNT_ACTIVATION_DAYS = 7
#REGISTRATION_AUTO_LOGIN = True
LOGIN_URL ='/nblik/login/'
LOGIN_REDIRECT_URL = '/nblik/next_step/'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UUID_LENGTH = 255
SOCIAL_AUTH_UID_LENGTH = 255
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 255
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 255
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 255
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 255
SOCIAL_AUTH_ENABLED_BACKENDS = ('google','facebook','linkedin','twitter')
GOOGLE_OAUTH2_CLIENT_ID = '110490777047-akrqtv142ehtq246eoa3lusf7pi1qk83.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '_KiK-17I-R6xNpGSmgOv0guV'
GITHUB_APP_ID = 'dc5dbf969550b54b6f1b'
GITHUB_API_SECRET = 'cfc368b681542a753b11a84a3d4d3e768204a03b'
SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'
FACEBOOK_APP_ID='714227718708789'
FACEBOOK_API_SECRET='10c08e65a84e063c86c0441292957e21'
FACEBOOK_EXTENDED_PERMISSIONS = ['email','publish_actions','public_profile']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'en_US'}
TWITTER_CONSUMER_KEY         = 'P2jkBWiMIQgiPFKzO4kRmefQA'
TWITTER_CONSUMER_SECRET      = 'X4LkTxItcTRIwGaYxn3WjPITzw2wdU2VMSiqh81daHBdzZDOkm'
LINKEDIN_CONSUMER_KEY        = '77ny0w4dfmmzci'
LINKEDIN_CONSUMER_SECRET     = 'f0IGt6awVN7F9dhT'
# Add email to requested authorizations.
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress',]
# Add the fields so they will be requested from linkedin.
#LINKEDIN_EXTRA_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
# Arrange to add the fields to UserSocialAuth.extra_data
#LINKEDIN_EXTRA_DATA = [('id', 'id'),
#                       ('first-name', 'first_name'),
#                       ('last-name', 'last_name'),
#                       ('email-address', 'email_address'),
#                       ('headline', 'headline'),
#                      ('industry', 'industry')]
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "blog_uploads/"
CKEDITOR_RESTRICT_BY_USER=True
CKEDITOR_BROWSE_SHOW_DIRS=True
AWS_QUERYSTRING_AUTH = False
CKEDITOR_ALLOW_NONIMAGE_FILES = False
# CKEDITOR_CONFIGS = {
#     'awesome_ckeditor': {
#         'toolbar': 'Basic',
#     },
# }
AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-us-west-2-031348677605'
AWS_ACCESS_KEY_ID = 'AKIAIGK3MBDZNNUI7OAQ'
AWS_SECRET_ACCESS_KEY = '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'

    # Tell django-storages that when coming up with the URL for an item in S3 storage, keep
    # it simple - just use this domain plus the path. (If this isn't set, things get complicated).
    # This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
    # We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    # This is used by the `static` template tag from `static`, if you're using that. Or if anything else
    # refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

    # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
    # you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# first define these settings in settings.py

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "nblikindia@gmail.com"
EMAIL_HOST_PASSWORD = "drzjjtxfowkpkhyj"
DEFAULT_FROM_EMAIL = "nblikindia@gmail.com"
DEFAULT_TO_EMAIL = 'to email' # don't change this
