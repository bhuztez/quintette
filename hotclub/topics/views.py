from quintette.views.generic import ListView, DetailView, CreateView
from quintette.contrib.auth.decorators import login_required

from hotclub.members.models import Member
from hotclub.topics.models import Topic
from hotclub.topics.forms import TopicForm


class list_topics(ListView):
    extra_context = {'navbar_selected': 'topics'}
    queryset = Topic.objects.exclude_subclasses()
    template_name = 'hotclub/topics/list-topics.html'


@login_required()
class post_new_topic(CreateView):
    extra_context = {'navbar_selected': 'topics'}
    form_class = TopicForm
    template_name = 'hotclub/topics/post-new-topic.html'


class view_topic(DetailView):
    extra_context = {'navbar_selected': 'topics'}
    queryset = Topic.objects.exclude_subclasses()
    pk_url_kwarg = 'topic_id'
    template_name = 'hotclub/topics/view-topic.html'

