from quintette.conf import settings
from quintette.contrib.auth import api


def user(request):
    if hasattr(request, 'user'):
        user = request.user
    else:
        fallback_backend = api.get_backend(settings.AUTH_FALLBACK_BACKEND_ALIAS)
        user = fallback_backend.get_user()

    return {'user': user}
