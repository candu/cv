from django.conf.urls.defaults import patterns, include, url
from django.contrib.sitemaps import Sitemap

class StaticSitemap(Sitemap):
  priority = 1.0
  lastmod = None

  def items(self):
    return ['/']

  def location(self, obj):
    return obj

sitemaps = {
  'static': StaticSitemap
}

urlpatterns = patterns('',
  (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
  url(r'^(.*)$', 'cv.views.index')
)
