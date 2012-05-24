from django.utils.functional import LazyObject
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule



class LazySettings(LazyObject):


    def _setup(self):
        from django.conf import settings
        self._wrapped = Settings(settings)



class Settings(object):

           
    def __init__(self, settings):
        self.settings = settings
        self.defaults = {}

        for app in self.INSTALLED_APPS:
            appmod = import_module(app)
            try:
                self.defaults[app.split('.')[-1].upper()] = import_module(app+'.settings')
            except ImportError:
                if module_has_submodule(appmod, 'settings'):
                    raise


    def __getattr__(self, name):
        if not name.isupper():
            raise AttributeError

        try:
            return getattr(self.settings, name)
        except AttributeError, e:
            parts = name.split('_')

            if len(parts) > 1:
                mod = self.defaults.get(parts[0], None)
                if mod:
                    try:
                        return getattr(mod, '_'.join(parts[1:]))
                    except AttributeError:
                        pass

            raise e



settings = LazySettings()



