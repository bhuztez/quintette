from django.db import models
from django.utils.translation import ugettext_lazy as _



class UsernameMixin(models.Model):
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'))

    class Meta:
        abstract = True



class EmailMixin(models.Model):
    email = models.EmailField(_('e-mail address'), blank=True)

    class Meta:
        abstract = True



class UniqueEmailMixin(models.Model):
    email = models.EmailField(_('e-mail address'), unique=True)

    class Meta:
        abstract = True



class NameMixin(models.Model):
    given_name = models.CharField(_('given name'), max_length=30, blank=True)
    surname = models.CharField(_('family name'), max_length=30, blank=True)

    class Meta:
        abstract = True


