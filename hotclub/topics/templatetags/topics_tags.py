from django import template
from django.contrib.contenttypes.models import ContentType
from quintette.contrib.favorites.models import Favorite

register = template.Library()


@register.assignment_tag
def get_watch_list(member, topics):
    if not member.is_authenticated():
        return {}

    return dict(Favorite.objects.filter(
        member=member,
        content_type__in=ContentType.objects.get_for_models(*topics).values(),
        object_id__in=[topic.id for topic in topics]).values_list('object_id', 'id'))


@register.assignment_tag
def get_is_watched(topic, watch_list):
    return watch_list.get(topic.id, None)


