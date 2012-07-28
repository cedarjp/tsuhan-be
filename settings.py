# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = '1!xm[i!%3yp$6sP|8,#7gB/:s4r>dKGs5>RdaD0+ bzqB=]J7-qwX8lv&|lIRDHD'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SESSION'

ADMINS = (
	('sugita','beat.s2000@gmail.com'),
)

TEMPLATE_DIRS = (
	'templates',
)

USE_I18N = False
DEFAULT_LANG = 'ja'

INSTALLED_APPS = (
  'kay.auth',
  'kay.ext.gaema',
  'core',
  'admin',
)

APP_MOUNT_POINTS = {
  'core':'/',
  'admin':'/admin',
}

# You can remove following settings if unnecessary.
CONTEXT_PROCESSORS = (
  'kay.context_processors.request',
  'kay.context_processors.url_functions',
  'kay.context_processors.media_url',
)
JINJA2_FILTERS = {
    'int_add_comma':'utils.int_add_comma',
    'is_none_empty':'utils.is_none_empty',
}

MIDDLEWARE_CLASSES = (
  'kay.auth.middleware.AuthenticationMiddleware',
  'kay.sessions.middleware.SessionMiddleware',
)
AUTH_USER_BACKEND = 'kay.auth.backends.googleaccount.GoogleBackend'
AUTH_USER_MODEL = 'tsuhanbe_auth.models.User'
SUBMOUNT_APPS = (
)

GAEMA_SECRETS = {
    'twitter_consumer_key': 'kIPoVXULkcHLJkxJ2Z7sw',
    'twitter_consumer_secret': '66cUOJdEmss2CNIlnaoLyYuRiVWe5cNi2RGCEhaubQ0',
}
# OAuth で使用するサービスを指定
# twitter や facebook など
# kay.ext.gaema.services に定義されている
GAEMA_VALID_SERVICES = [
    'twitter',
]