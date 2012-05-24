from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^forum_project/', include('forum_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('quintette.contrib.password_auth.urls')),
    url(r'^', include('hotclub.urls')),
    url(r'^', include('hotclub.topics.urls')),
    url(r'^', include('hotclub.answers.urls')),

)


