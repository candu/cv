from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tags/$', 'cv.views.ajax.tags'),
    url(r'^$', 'cv.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
