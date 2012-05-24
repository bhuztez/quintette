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
       self.defaults = []

       for app in self.INSTALLED_APPS:
           appmod = import_module(app)
           try:
               self.defaults.append(import_module(app+'.global_settings'))
           except ImportError:
               if module_has_submodule(appmod, 'global_settings'):
                   raise


   def __getattr__(self, name):
       if not name.isupper():
           raise AttributeError

       try:
           return getattr(self.settings, name)
       except AttributeError, e:
           for mod in self.defaults:
               try:
                   return getattr(mod, name)
               except AttributeError:
                   pass

           raise e



settings = LazySettings()



class LazyNamespace(LazyObject):

    def __init__(self, name, verbose_name):
        self.__dict__['name'] = name
        self.__dict__['verbose_name'] = verbose_name
        self._wrapped = None


    def _setup(self):
        self._wrapped = Namespace(self.name)



class Namespace(object):

    def __init__(self, name):
        namespaces_mod = import_module('namespaces')
        try:
            self.mod = import_module('namespaces.'+name)
        except ImportError:
            if module_has_submodule('namespaces', name):
                raise


    def __getattr__(self, name):
        if not name.isupper():
            raise AttributeError

        return getattr(self.mod, name)



class LazyNamespaces(LazyObject):

    def _setup(self):
        self._wrapped = Namespaces()



class Namespaces(object):

    def __init__(self):
        self._namespaces = dict(
            (k, LazyNamespace(k, v)) for k,v in settings.NAMESPACES )

    
    def __getattr__(self, name):
        try:
            return self._namespaces[name]
        except KeyError:
            raise AttributeError



namespaces = LazyNamespaces()







