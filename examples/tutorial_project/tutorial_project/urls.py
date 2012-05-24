from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^poll1/', include('poll1.urls')),
    url(r'^poll2/', include('poll2.urls')),
)

