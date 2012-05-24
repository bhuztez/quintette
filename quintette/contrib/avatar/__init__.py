from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from quintette.conf import settings


def load_provider(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]

    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing avatar providers %s: "%s"' % (path, e))
    except ValueError, e:
        raise ImproperlyConfigured('Error importing avatar providers. Is AVATAR_PROVIDERS a correctly defined list or tuple?')

    try:
        provider = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" avatar provider' % (module, attr))

    return provider()



def get_providers():
    providers = [ load_provider(path) for path in settings.AVATAR_PROVIDERS ]

    if not providers:
        raise ImproperlyConfigured('No avatar providers have been defined. Does AVATAR_PROVIDERS contain anything?')

    return providers


