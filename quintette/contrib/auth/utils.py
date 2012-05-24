import threading

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.db.models import get_model

from quintette.conf import settings


def load_anonymous_user_class():
    path = settings.AUTH_ANONYMOUS_USER_CLASS
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    
    return getattr(import_module(module), attr)


def login(request, user, realm):
    if user is None:
        user = request.user

    if (( settings.AUTH_SESSION_KEY in request.session ) or
        ( settings.AUTH_REALM_SESSION_KEY in request.session )):
        if ((request.session.get(settings.AUTH_SESSION_KEY, None) != user.id) or
            (request.session.get(settings.AUTH_REALM_SESSION_KEY, None) != realm)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    request.session[settings.AUTH_SESSION_KEY] = user.id
    request.session[settings.AUTH_REALM_SESSION_KEY] = realm

    if hasattr(request, 'user'):
        request.user = user
    # user_logged_in.send(sender=user.__class__, request=request, user=user)



def logout(request, realm=None):

    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None

    # user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()

    if hasattr(request, 'user'):
        user_class = load_anonymous_user_class()
        return user_class(request)


def get_realm(request):
    return request.session.get(settings.AUTH_REALM_SESSION_KEY, None)


def get_user(request, user_model=None, fallback=True):
    user_id = request.session.get(settings.AUTH_SESSION_KEY, None)
    realm_alias = request.session.get(settings.AUTH_REALM_SESSION_KEY, None)

    if user_id is not None and realm_alias is not None:
        if realm_alias in settings.AUTH_REALMS:
            realm_user_model = get_model(*settings.AUTH_REALMS[realm_alias]['MODEL'].rsplit('.', 1))

            if user_model is None:
                user_model = realm_user_model
            elif not issubclass(user_model, realm_user_model):
                raise ImproperlyConfigured

            try:
                return user_model.objects.get(pk=user_id)
            except user_model.DoesNotExist:
                pass
        else:
            request.session.flush()

    if fallback:
        user_class = load_anonymous_user_class()
        return user_class(request)



