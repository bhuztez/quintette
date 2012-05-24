from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.db.models.sql.where import Constraint, AND
from django.contrib.contenttypes.models import ContentType

from quintette.contrib.auth.backends import Backend
from quintette.contrib.password_auth.models import Credential



class DatabasePasswordAuth(object):

    def authenticate(self, login, password, realm):
        content_type = ContentType.objects.get_for_model(self.user_model)

        qs = Credential.objects.filter(content_type = content_type)

        # use undocumented API is bad, but hard-coding is even worse
        alias = qs.query.join((
                Credential._meta.db_table,
                self.user_model._meta.db_table,
                Credential.user_object.fk_field,
                'id'))

        qs.query.where.add(
            ( Constraint (
                    alias,
                    self.login_field,
                    self.user_model._meta.get_field_by_name(self.login_field)[0]),
              'exact',
              login),
            AND)

        credential = qs.get()

        if credential.check_password(password):
            return credential.user_object


