from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^(.*)$', 'cv.views.index'),
)
