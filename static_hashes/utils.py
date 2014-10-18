from django.conf import settings
import json


if hasattr(settings, 'STATIC_HASHES_STATIC_DIRS'):
    STATIC_DIRS = settings.STATIC_HASHES_STATIC_DIRS
else:
    STATIC_DIRS = settings.STATICFILES_DIRS


def get_current_hash():
    """returns newsest commit hash"""
    try:
        with open(settings.STATIC_HASHES_OUTPUT_JSON, 'r') as f:
            return json.loads(f.read())['__current__']
    except IOError:
        return ''


def local_to_browser_path(path):
    for static_dir in STATIC_DIRS:
        if static_dir in path:
            return path.replace(static_dir, settings.STATIC_URL).replace('//', '/')