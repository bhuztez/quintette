from django.conf.urls import patterns, include, url

urlpatterns = patterns('hotclub.answers.views',

    url(r'^questions/$',
        'list_questions',
        name='hotclub-answers-list-questions'),

    url(r'^question/(?P<question_id>\d+)/$',
        'view_question',
        name='hotclub-answers-view-question'),

)

