from django.conf.urls import patterns, include, url


urlpatterns = patterns('hotclub.views',

    url(r'^$',
        'list_all',
        name='hotclub-list-all'),

)

