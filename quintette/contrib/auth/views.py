import urlparse

from django import http

from quintette.conf import settings


def redirect_to_login(request, realm=None):
    path = request.build_absolute_uri()

    if realm is None:
        login_url = settings.AUTH_LOGIN_URL
        if login_url is None:
            login_url = settings.AUTH_REALMS[settings.AUTH_DEFAULT_REALM_ALIAS]['LOGIN_URL']
    else:
        login_url = settings.AUTH_REALMS[realm]['LOGIN_URL']

    login_scheme, login_netloc = urlparse.urlparse(login_url)[:2]
    current_scheme, current_netloc = urlparse.urlparse(path)[:2]

    if ((not login_scheme or login_scheme == current_scheme) and
        (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()

    parts = list(urlparse.urlparse(login_url))
    
    querystring = http.QueryDict(parts[4], mutable=True)
    querystring[settings.AUTH_REDIRECT_FIELD_NAME] = path 
    parts[4] = querystring.urlencode(safe='/')
    
    return http.HttpResponseRedirect(urlparse.urlunparse(parts))

