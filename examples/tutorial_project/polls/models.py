import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

app_label = __package__.split('.')[-1]

class Poll(models.Model):
    question = models.CharField(_("question"), max_length=200)
    pub_date = models.DateTimeField(_("date published"))

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = _("poll")
        verbose_name_plural = _("polls")

    def was_published_recently(self):
        return self.pub_date >= ( timezone.now() - datetime.timedelta(days=1) )

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = _('Published recently?')

    @models.permalink
    def get_absolute_url(self):
        return (app_label + '-poll-detail', [self.pk])

    @models.permalink
    def get_vote_url(self):
        return (app_label + '-poll-vote', [self.pk])

    @models.permalink
    def get_results_url(self):
        return (app_label + '-poll-results', [self.pk])


class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_("poll"))
    choice = models.CharField(_("choice"), max_length=200)
    votes = models.IntegerField(_("votes"), default=0)

    def __unicode__(self):
        return self.choice

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")

