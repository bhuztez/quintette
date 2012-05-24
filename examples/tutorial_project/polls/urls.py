from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from .models import Poll

app_label = __package__.split('.')[-1]

urlpatterns = patterns(__package__+'.views',

    url(r'^$',
        ListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name= app_label + '/index.html'),
        name=app_label+'-index'),

    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Poll,
            template_name= app_label + '/detail.html'),
        name=app_label+'-poll-detail'),

    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Poll,
            template_name= app_label + '/results.html'),
        name=app_label+'-poll-results'),

    url(r'^(?P<poll_id>\d+)/vote/$',
        'vote',
        name=app_label+'-poll-vote'),

)

