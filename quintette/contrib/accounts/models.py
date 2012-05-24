from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from quintette.conf import settings
from quintette.db.models import Model


class UserProfile(Model):
    __mixins__ = settings.PROFILE_MIXINS

    user = models.OneToOneField(User, verbose_name=_("user"))

    def __unicode__(self):
        return self.user.username
        
    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")


