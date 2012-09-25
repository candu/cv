from xhpy.pylib import *

from django.http import HttpResponse

from cv.models import Content, Tag
from cv.ui.content import :ui:content
from cv.ui.layout import :ui:two-columns
from cv.ui.page import :ui:page
from cv.ui.tag import :ui:tag

def index(request, tag_spec):
  selected_tags = set()
  for name in tag_spec.split('/'):
    try:
      selected_tags.add(Tag.objects.get(name=name))
    except Tag.DoesNotExist:
      pass
  tags = Tag.objects.all()
  contents = sorted(
      Content.objects.all(), key=lambda c: c.finished, reverse=True)
  print_header = \
  <div class="UIPrintHeader">
    <div class="UIPrintName">Evan Savage</div>
    <div class="UIPrintCoordinates">
      savage.evan<span class="grey">@gmail.com</span>
    </div>
  </div>
  left_ranked = <div class="UILeftRanked" />
  right_ranked = <div class="UIRightRanked" />
  for c in contents:
    right_ranked.appendChild(<ui:content content={c} />)
  page = \
  <ui:page title="Evan Stratford :: CV">
    <div class="UIHeader">
      {print_header}
    </div>
    <ui:two-columns>
      {left_ranked}
      {right_ranked}
    </ui:two-columns>
  </ui:page>
  return HttpResponse(page)
