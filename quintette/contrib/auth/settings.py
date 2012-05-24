SESSION_KEY = '_quintette_auth_user_id'
REALM_SESSION_KEY = '_quintette_auth_user_realm'
REDIRECT_FIELD_NAME = 'next'


DEFAULT_REALM_ALIAS = 'default'


REALMS = {
    'default': {
        'MODEL': 'auth.user',
        'PASSWORD_AUTH_LOGIN_FIELD': 'username',
        'LOGIN_URL': None,
        'LOGOUT_URL': None,
        'LOGIN_REDIRECT_URL': None,
        'AUTHENTICATION_BACKENDS': (
            'quintette.contrib.password_auth.backends.DatabasePasswordAuth',
        ),
    },
}


LOGIN_URL = None
LOGOUT_URL = None
LOGIN_REDIRECT_URL = None
ANONYMOUS_USER_CLASS = 'quintette.contrib.auth.users.AnonymousUser'


USER_MODEL_MIXINS = (
    'quintette.contrib.auth.model_mixins.UsernameMixin',
)



