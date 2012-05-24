from quintette.db import models
from django.utils.translation import ugettext_lazy as _

from hotclub.topics.models import Topic


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    topics = models.ManyToManyField(Topic, related_name='tags')

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

