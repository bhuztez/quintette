from quintette.db import models
from django.utils.translation import ugettext_lazy as _	
from hotclub.topics.models import Topic


class Question(Topic):

    @models.permalink
    def get_absolute_url(self):
        return ('hotclub-answers-view-question', (self.id,), {})

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
