from xhpy.pylib import *

from django.http import HttpResponse

from cv.models import Content, Tag
from cv.ui.activity import :ui:activity
from cv.ui.layout import :ui:two-columns
from cv.ui.page import :ui:page
from cv.ui.typeahead import :ui:typeahead

def index(request):
  tags = Tag.objects.all()
  contents = Content.objects.all()
  activities = sorted(
      [c for c in contents if c.content_type == Content.ACTIVITY],
      key=lambda c: c.finished,
      reverse=True)
  controls = \
  <div class="UIControlsHeader">
    <div class="UIControls">
      <div class="UILeftTypeahead">
        <ui:typeahead />
      </div>
      <div class="UIRightTypeahead">
        <ui:typeahead />
      </div>
    </div>
  </div>
  bottom_ranked = <div class="UIBottomRanked" />
  for activity in activities:
    bottom_ranked.appendChild(<ui:activity activity={activity} />)
  page = \
  <ui:page title="Evan Stratford :: CV">
    <ui:two-columns>
      {controls}
      <div class="UILeftRanked" />
      <div class="UIRightRanked" />
      {bottom_ranked}
    </ui:two-columns>
  </ui:page>
  return HttpResponse(page)
