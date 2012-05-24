from quintette.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from hotclub.members.models import Member


class Favorite(models.Model):
    member = models.ForeignKey(Member, related_name='favorites')

    content_type   = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField(_('object ID'))
    favorite_object = generic.GenericForeignKey("content_type", "object_id")


    class Meta:
        unique_together = ('member', 'content_type', 'object_id')
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')

