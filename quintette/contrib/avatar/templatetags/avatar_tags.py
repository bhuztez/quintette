from django import template
from django.core.exceptions import ImproperlyConfigured

from quintette.conf import settings
from quintette.contrib.avatar import get_providers

register = template.Library()


@register.simple_tag
def avatar(user, size=None):
    if size is None:
        size = settings.AVATAR_DEFAULT_SIZE

    if isinstance(size, int) or isinstance(size, long):
        if not (0 < size <= settings.AVATAR_MAX_SIZE):
            raise ImproperlyConfigured
    else:
        try:
            size = settings.AVATAR_SIZES[size]
        except KeyError:
            raise ImproperlyConfigured
    
    for provider in providers:
        result = provider.get_avatar_url(user, size)
        if result:
            return result

    if not settings.AVATAR_DEFAULT_AVATAR:
        raise ImproperlyConfigured('No default avatar has been defined. Does AVATAR_DEFAULT_AVATAR contain anything?')

    return settings.AVATAR_DEFAULT_AVATAR




