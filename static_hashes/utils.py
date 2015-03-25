from django.conf import settings
import json
import os


if hasattr(settings, 'STATIC_HASHES_STATIC_DIRS'):
    STATIC_DIRS = settings.STATIC_HASHES_STATIC_DIRS
else:
    STATIC_DIRS = settings.STATICFILES_DIRS


def get_current_hash():
    """returns newsest commit hash"""
    try:
        static_hashes_json = os.path.join(settings.STATIC_HASHES_OUTPUT_DIR, 'static-hashes.json')
        with open(static_hashes_json, 'r') as f:
            return json.loads(f.read())['__current__']
    except IOError:
        return ''


def local_to_browser_path(path):
    for static_dir in STATIC_DIRS:
        custom_root = static_dir.get('custom_root', None)
        static_dir = static_dir['dir']
        if static_dir in path:
            if not custom_root:
                return path.replace(static_dir, settings.STATIC_URL).replace('//', '/')
            else:
                return path.replace(static_dir, custom_root)
