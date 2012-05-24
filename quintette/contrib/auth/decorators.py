from functools import wraps

from django import http
from django.core.exceptions import PermissionDenied

from quintette.conf import settings
from quintette.contrib.auth import api


def cast_user_model(model):

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # XXX
            request.user.__class__ = model
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def login_required(realm=None, redirect=True):

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if (realm is None) or (request.auth_realm == realm):
                if request.user.is_authenticated():
                    return func(request, *args, **kwargs)
            
            if not redirect:
                raise PermissionDenied
                
            from quintette.contrib.auth.views import redirect_to_login
            return redirect_to_login(request, realm)

        return wrapper

    return decorator

