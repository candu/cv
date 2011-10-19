from django.http import HttpResponse

from cv.models import Content, Tag
from cv.ui.page import :ui:page
from cv.ui.timeline import :ui:timeline
from cv.ui.typeahead import :ui:typeahead

def index(request):
  tags = Tag.objects.all()
  contents = Content.objects.all()
  page = \
  <ui:page title="Evan Stratford :: CV">
    <ui:timeline contents={contents} />
  </ui:page>
  return HttpResponse(page)

def typeahead_test(request):
  print 'loaded typeahead_test view'
  page = \
  <ui:page title="Typeahead Test">
    <ui:typeahead />
  </ui:page>
  return HttpResponse(page)
