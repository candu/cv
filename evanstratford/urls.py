from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^similar_content/(\d+)/$', 'cv.views.ajax.similar_content'),
    url(r'^$', 'cv.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
