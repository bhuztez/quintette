from quintette.views.generic import ListView
from hotclub.topics.models import Topic


class list_all(ListView):
    extra_context = {'navbar_selected': 'all'}
    queryset = Topic.objects.select_related_with_subclasses("author").prefetch_related("tags").order_by('-submit_time')
    template_name = 'hotclub/topics/list-topics.html'


