from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^similar_content/(\d+)/$', 'cv.views.ajax.similar_content'),
    url(r'^tags/$', 'cv.views.ajax.tags'),
    url(r'^typeahead_test/$', 'cv.views.typeahead_test'),
    url(r'^$', 'cv.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
