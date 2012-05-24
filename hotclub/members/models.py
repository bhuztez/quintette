from quintette.conf import settings
from quintette.db import models

from django.utils.translation import ugettext_lazy as _



class Member(models.Model):
    __mixins__ = settings.HOTCLUB_MEMBER_MODEL_MIXINS

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __unicode__(self):
        return self.username


    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")



