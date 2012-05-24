import urlparse

from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass 
from django.forms.models import fields_for_model
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.db.models import get_model
from quintette.conf import settings
from quintette.contrib.auth import api

from django.contrib.contenttypes.models import ContentType
from quintette.contrib.password_auth.models import Credential
from django.db.models.sql.where import Constraint, AND


def authenticate(login, password, realm):
    conf = settings.AUTH_REALMS[realm]
    user_model = get_model(*conf['MODEL'].rsplit('.', 1))
    login_field = conf['PASSWORD_AUTH_LOGIN_FIELD']

    content_type = ContentType.objects.get_for_model(user_model)

    qs = Credential.objects.filter(content_type = content_type)

    # use undocumented API is bad, but hard-coding is even worse
    alias = qs.query.join((
            Credential._meta.db_table,
            user_model._meta.db_table,
            Credential.user_object.fk_field,
            'id'))

    qs.query.where.add(
        ( Constraint (
                alias,
                login_field,
                user_model._meta.get_field_by_name(login_field)[0]),
          'exact',
          login),
        AND)

    credential = qs.get()

    if credential.check_password(password):
        return credential.user_object




class AuthenticationForm(forms.Form):

    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
    }


    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)


    def clean(self):
        login_field = settings.AUTH_REALMS[self._realm]['PASSWORD_AUTH_LOGIN_FIELD']

        login = self.cleaned_data.get(login_field)
        password = self.cleaned_data.get('password')

        if login and password:
            self.user_cache = authenticate(login, password, self._realm)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])

        self.check_for_test_cookie()
        return self.cleaned_data


    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])


    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None


    def get_user(self):
        return self.user_cache



def get_auth_form_class(realm_alias):
    conf = settings.AUTH_REALMS[realm_alias]
    user_model = get_model(*conf['MODEL'].rsplit('.', 1))
    login_field = conf['PASSWORD_AUTH_LOGIN_FIELD']

    attrs = fields_for_model(
        user_model,
        (login_field,))

    attrs['password'] = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    attrs['_realm'] = realm_alias

    return DeclarativeFieldsMetaclass(
        '%sLoginForm'%(realm_alias.capitalize()),
        (AuthenticationForm,),
        attrs)

redirect_field_name = settings.AUTH_REDIRECT_FIELD_NAME


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request,
          realm_alias=None):
    if realm_alias is None:
        realm_alias = settings.AUTH_DEFAULT_REALM_ALIAS

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    authentication_form = get_auth_form_class(realm_alias)

    if request.method == "POST":
        form = authentication_form(data=request.POST)

        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]
            
            login_redirect_url = settings.AUTH_REALMS[realm_alias].get('LOGIN_REDIRECT_URL', settings.AUTH_LOGIN_REDIRECT_URL)

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = login_redirect_url
            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = login_redirect_url

            # Okay, security checks complete. Log the user in.
            api.login(request, form.get_user(), realm_alias)

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    context = {
        'form': form,
        redirect_field_name: redirect_to,
    }

    template_list = [
        'auth/%s/login.html'%(realm_alias),
        'auth/login.html',
    ]

    return TemplateResponse(request, template_list, context)



def logout(request, realm_alias=None):
    if realm_alias is None:
        realm_alias = settings.AUTH_DEFAULT_REALM_ALIAS

    api.logout(request, realm_alias)

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Security check -- don't allow redirection to a different host.
        if not (netloc and netloc != request.get_host()):
            return HttpResponseRedirect(redirect_to)

    template_list = [
        'auth/%s/logged_out.html'%(realm_alias),
        'auth/logged_out.html',
    ]

    return TemplateResponse(request, template_list, {})



