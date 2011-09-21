from django.http import HttpResponse

from cv.models import Tag
from cv.ui.page import :ui:page
from cv.ui.tags import :ui:tags

def index(request):
  tags = Tag.objects.all()
  page = \
  <ui:page title="Evan Stratford :: CV">
    <ui:tags tags={tags} />
  </ui:page>
  return HttpResponse(page)
