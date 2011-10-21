from xhpy.pylib import *

from django.http import HttpResponse

from cv.models import Content, Tag
from cv.ui.activity import :ui:activity
from cv.ui.layout import :ui:two-columns
from cv.ui.page import :ui:page

def index(request):
  tags = Tag.objects.all()
  contents = Content.objects.all()
  activities = sorted(contents, key=lambda c: c.finished, reverse=True)
  controls = \
  <div class="UIControlsHeader">
  </div>
  right_ranked = <div class="UIRightRanked" />
  for activity in activities:
    right_ranked.appendChild(<ui:activity activity={activity} />)
  page = \
  <ui:page title="Evan Stratford :: CV">
    <ui:two-columns>
      {controls}
      <div class="UILeftRanked hidden" />
      {right_ranked}
    </ui:two-columns>
  </ui:page>
  return HttpResponse(page)
