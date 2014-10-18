import os

from django import template
from django.conf import settings

from static_hashes import utils

register = template.Library()

@register.simple_tag
def get_static_hashes(*args, **kwargs):
    path = utils.local_to_browser_path(
        os.path.join(settings.PROJECT_PATH, settings.STATIC_HASHES_OUTPUT_JS)
    )
    hash = utils.get_current_hash()
    tmpl = '<script type="text/javascript" src="{path}?hash={hash}"></script>'
    return tmpl.format(path=path, hash=hash)