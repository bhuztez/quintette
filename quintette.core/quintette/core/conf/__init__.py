from django.conf import settings
from django.core.exceptions import ImproperlyConfigured



class AppSettings(object):

    def __init__(self, package=None, **kwargs):
        if package is None:
            package = self.__module__

            if package == __package__ or '.' not in package:
                raise ImproperlyConfigured

            package = self.__module__.rsplit('.', 1)[0]

        self.package = package

        for key,value in kwargs.items():
            if key.isupper():
                setattr(self, key, value)


    def __getattribute__(self, name):
        if not name.isupper():
            return object.__getattribute__(self, name)

        try:
            default = object.__getattribute__(self, name)
        except:
            raise
        else:
            return getattr(
                settings,
                '{0}_{1}'.format(
                    self.package.replace('.', '_'),
                    name),
                default)


