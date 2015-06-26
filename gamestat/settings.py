"""
Django settings for gamestat project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c60n1%uxdck1)!+mvsn$kz_n$8dd(ut7v%f%(sr811fu8w*r+7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['iizs.net']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'twitter_bootstrap',
    'wget',
    'kbo',
    'ui',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gamestat.urls'

WSGI_APPLICATION = 'gamestat.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR,'my.cnf'),
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/gamestat/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_DIRS = ( os.path.join(BASE_DIR,'static') )
#STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# Pipeline
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_ENABLED = True
PIPELINE_DISABLE_WRAPPER = True

import twitter_bootstrap
bootstrap_less = os.path.join(os.path.dirname(twitter_bootstrap.__file__), 'static', 'less')

PIPELINE_LESS_ARGUMENTS = u'--include-path={}'.format(
    os.pathsep.join([
        bootstrap_less,
    ])
)

PIPELINE_CSS = {
    'starter-template': {
        'source_filenames': (
            'ui/css/starter-template.css',
        ),
        'output_filename': 'css/starter-template.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'bootstrap': {
        'source_filenames': (
            'twitter_bootstrap/less/bootstrap.less',
        ),
        'output_filename': 'css/bootstrap.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_JS = {
    'bootstrap': {
        'source_filenames': (
            'twitter_bootstrap/js/transition.js',
            'twitter_bootstrap/js/modal.js',
            'twitter_bootstrap/js/dropdown.js',
            'twitter_bootstrap/js/scrollspy.js',
            'twitter_bootstrap/js/tab.js',
            'twitter_bootstrap/js/tooltip.js',
            'twitter_bootstrap/js/popover.js',
            'twitter_bootstrap/js/alert.js',
            'twitter_bootstrap/js/button.js',
            'twitter_bootstrap/js/collapse.js',
            'twitter_bootstrap/js/carousel.js',
            'twitter_bootstrap/js/affix.js',
        ),
        'output_filename': 'js/bootstrap.js',
    },
}

# Template
ROOT_TEMPLATE = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = [
    ROOT_TEMPLATE,
]

