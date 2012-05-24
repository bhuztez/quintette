from django.conf.urls import patterns, include, url


urlpatterns = patterns('hotclub.topics.views',

    url(r'^topics/$',
        'list_topics',
        name='hotclub-topics-list-topics'),

    url(r'^topic/(?P<topic_id>\d+)/$',
        'view_topic',
        name='hotclub-topics-view-topic'),

    # url(r'^reply/(?P<topic_id>\d+)/(?P<reply_id>\d+)/$',
    #     'post_reply',
    #     name='hotclub-topics-view-reply'),

    url(r'^new-topic/$',
        'post_new_topic',
         name='hotclub-topics-post-new-topic'),

    # url(r'^reply/(?P<topic_id>\d+)/$',
    #     'post_reply',
    #     name='hotclub-topics-post-reply'),
)

