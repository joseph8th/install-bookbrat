# DEVELOPMENT
# NOTE: Exclude this file from version control to maintain local/remote settings.
#
# Django settings for bookbrat project
# By Joseph Edwards VIII (joseph8th@notroot.us)

from os.path import join

# See 'settings_common.py' for common settings.
# I import all '*' here ONLY and promise to import variables the rest of the time. :)
from settings_common import *

DEBUG = True             # set True for dev environment
TEMPLATE_DEBUG = DEBUG

# Set to 'sqlite3' for dev, and 'postgresql_psycopg2' for production
DATABASES = {
    'default': {

        # Change to 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle', depending:
        'ENGINE':   'django.db.backends.sqlite3',

        'NAME':     'sqlite3.db',
        'USER':     '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST':     '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT':     '',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Root URL that handles project apps server (dev or production). No trailing slash.
# Example: "http://my_app.local" OR "https://my_app.com" (dev or production)
APP_URL = 'http://bookbrat.local'

# Root absolute path to the directory for STATIC_ROOT and MEDIA_ROOT static app.
# Example: "/var/www/my_app"
STATIC_APP_ROOT = '/var/www/bookbrat'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Note this is in the root of the static app directory!
MEDIA_ROOT = "%s/" % (join( STATIC_APP_ROOT, 'media' ))

# URL that handles the media served from MEDIA_ROOT. Just change the 2nd parameter.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "%s/%s/" % ( APP_URL, 'media' )

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "%s/" % (join( STATIC_APP_ROOT, 'static' ))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "%s/%s/" % ( APP_URL, 'static' )

# Additional locations of static files. Then 'manage.py collectstatic'.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS += ('debug_toolbar',)