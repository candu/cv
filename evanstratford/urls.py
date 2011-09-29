from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^similar_tags/(\d+)/$', 'cv.views.ajax.similar_tags'),
    url(r'^$', 'cv.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
