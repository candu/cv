from xhpy.pylib import *

from django.http import HttpResponse

from cv.models import Content, Tag
from cv.ui.content import :ui:content
from cv.ui.layout import :ui:two-columns
from cv.ui.page import :ui:page

def index(request):
  tags = Tag.objects.all()
  contents = sorted(
      Content.objects.all(), key=lambda c: c.finished, reverse=True)
  controls = \
  <div class="UIControlsHeader">
  </div>
  right_ranked = <div class="UIRightRanked" />
  for content in contents:
    right_ranked.appendChild(<ui:content content={content} />)
  page = \
  <ui:page title="Evan Stratford :: CV">
    <ui:two-columns>
      {controls}
      <div class="UILeftRanked hidden" />
      {right_ranked}
    </ui:two-columns>
  </ui:page>
  return HttpResponse(page)
