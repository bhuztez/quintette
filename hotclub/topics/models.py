from quintette.db import models
from django.utils.translation import ugettext_lazy as _

from hotclub.members.models import Member
# from hotclub.tags.models import Tag


class TopicQuerySet(models.QuerySet):


    def _get_subclasses(self, *subclasses):
        return tuple( rel.var_name
            for rel in self.model._meta.get_all_related_objects()
                if isinstance(rel.field, models.OneToOneField)
                and issubclass(rel.field.model, self.model) )


    def select_related_with_subclasses(self, *fields):
        subclasses = self._get_subclasses()
        new_qs = self.select_related(*(fields + subclasses))
        new_qs.subclasses = subclasses
        return new_qs
    

    def exclude_subclasses(self):
        subclasses = self._get_subclasses()
        return self.filter(**dict( (subclass, None)
            for subclass in subclasses))


    def _clone(self, klass=None, setup=False, **kwargs):
        for name in ['subclasses', '_annotated']:
            if hasattr(self, name):
                kwargs[name] = getattr(self, name)
        return super(TopicQuerySet, self)._clone(klass, setup, **kwargs)


    def annotate(self, *args, **kwargs):
        qset = super(TopicQuerySet, self).annotate(*args, **kwargs)
        qset._annotated = [a.default_alias for a in args] + kwargs.keys()
        return qset


    def iterator(self):
        iter = super(TopicQuerySet, self).iterator()
        if getattr(self, 'subclasses', False):
            for obj in iter:
                sub_obj = [getattr(obj, s) for s in self.subclasses if getattr(obj, s)] or [obj]
                sub_obj = sub_obj[0]
                if getattr(self, '_annotated', False):
                    for k in self._annotated:
                        setattr(sub_obj, k, getattr(obj, k))

                yield sub_obj
        else:
            for obj in iter:
                yield obj



class TopicManager(models.Manager):

    def get_query_set(self):
        return TopicQuerySet(self.model)

    def select_related_with_subclasses(self, *fields):
        return self.get_query_set().select_related_with_subclasses(*fields)

    def exclude_subclasses(self):
        return self.get_query_set().exclude_subclasses()



class Topic(models.Model):
    objects = TopicManager()

    title = models.CharField(_('title'), max_length=255)
    content = models.TextField(_('content'))

    author = models.ForeignKey(Member, related_name='topics', verbose_name=_('author'))
    submit_time = models.DateTimeField(auto_now_add=True)
    last_reply_time = models.DateTimeField(null=True, blank=True, default=None)

    # tags = models.ManyToManyField(Tag, related_name='threads')

    reply_count = models.IntegerField(default=0)

    # score = models.FloatField()
    # hot = models.FloatField()
    
    @models.permalink
    def get_absolute_url(self):
        return ('hotclub-topics-view-topic', (self.id,), {})


    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')



class Reply(models.Model):
    thread = models.ForeignKey(Topic, related_name='replies')
    reply_to = models.ForeignKey('self', blank=True, null=True)
    content = models.TextField()

    author = models.ForeignKey(Member, related_name='replies')
    submit_time = models.DateTimeField()

    # score = models.FloatField()


    class Meta:
        verbose_name = _('reply')
        verbose_name_plural = _('replies')


