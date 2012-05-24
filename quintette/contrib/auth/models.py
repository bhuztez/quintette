from django.utils.translation import ugettext_lazy as _

from quintette.conf import settings
from quintette.db import models


class User(models.Model):
    __mixins__ = settings.AUTH_USER_MODEL_MIXINS


    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


    class Meta:
        abstract = True
        verbose_name = _("user")
        verbose_name_plural = _("users")

