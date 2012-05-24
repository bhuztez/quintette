import operator

from django.utils.functional import SimpleLazyObject, new_method_proxy, empty

from quintette.conf import settings
from quintette.contrib.auth import api



def _set_user_model(self, model):
    self._wrapped_model = model


class LazyUserObject(SimpleLazyObject):

    def __init__(self, func):
        super(LazyUserObject, self).__init__(func)
        self._wrapped_model = None


    def __setattr__(self, name, value):
        if name.startswith("_wrapped"):
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__[name] = value
        elif name == '__class__':
            object.__setattr__(self, name, value)
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)


    def _setup(self):
        self._wrapped = self._setupfunc(self._wrapped_model)


    __class__ = property(
        new_method_proxy(operator.attrgetter("__class__")),
        _set_user_model)



def get_user(request, model=None):
    if not hasattr(request, '_quintette_cached_user'):
        request._quintette_cached_user = api.get_user(request, model)
        
    return request._quintette_cached_user


def get_auth_realm(request):
    if not hasattr(request, '_quintette_cached_realm'):
        request._quintette_cached_realm = api.get_realm(request)

    return request._quintette_cached_realm
    


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Quintette authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.user = LazyUserObject(lambda model: get_user(request, model))
        
        request.auth_realm = SimpleLazyObject(lambda: get_auth_realm(request))



# class AuthenticationMiddleware(object):

#     def process_request(self, request):
#         assert hasattr(request, 'session'), "The Quintette authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

#         request.user = SimpleLazyObject(lambda model: get_user(request, settings.USER_MODEL))


