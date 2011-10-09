from django.http import HttpResponse

from cv.models import Content, Tag
from cv.ui.layout import :ui:two-column-layout
from cv.ui.page import :ui:page
from cv.ui.tags import :ui:tags
from cv.ui.timeline import :ui:timeline

def index(request):
  tags = Tag.objects.all()
  contents = Content.objects.all()
  page = \
  <ui:page title="Evan Stratford :: CV">
    <ui:two-column-layout>
      <ui:tags tags={tags} />
      <ui:timeline contents={contents} />
    </ui:two-column-layout>
  </ui:page>
  return HttpResponse(page)
