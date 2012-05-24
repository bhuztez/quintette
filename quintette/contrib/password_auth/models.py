from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.hashers import check_password, make_password


class Credential(models.Model):
    content_type   = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_id      = models.TextField(_('object ID'))
    user_object = generic.GenericForeignKey("content_type", "object_id")

    password = models.CharField(_('password'), max_length=128)


    class Meta:
        unique_together = ('content_type', 'object_id')
        verbose_name = _("credential")
        verbose_name_plural = _("credentials")


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)
        

