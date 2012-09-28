from xhpy.pylib import *

from django.http import HttpResponse

from cv.models import Content, Tag
from cv.ui.banner import :ui:banner
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
  categories = [
    ('languages', ('bash', 'C', 'C++', 'Java', 'JavaScript', 'PHP', 'Python')),
    ('technical', (
      'Algorithms',
      'Mathematics',
      'Machine Learning',
      'Real-Time Computing',
      'Open-Source',
      'Web Development'
    )),
    ('personal', (
      'Awards',
      'Communication',
      'Fitness',
      'Music',
      'Travel',
      'Volunteer Work'
    ))
  ]
  contents = sorted(
      Content.objects.all(), key=lambda c: c.finished, reverse=True)
  coordinates = [
    ('email', 'savage.evan@gmail.com', 'mailto:savage.evan@gmail.com'),
    ('facebook', 'savage.evan', 'http://facebook.com/savage.evan'),
    ('linkedin', 'evansavage', 'http://linkedin.com/in/evansavage'),
    ('github', 'candu', 'http://github.com/candu'),
  ]
  banner = \
  <ui:banner name="Evan Savage" coordinates={coordinates} tags={tags} categories={categories}/>
  left_ranked = <div class="UILeftRanked" />
  right_ranked = <div class="UIRightRanked" />
  for c in contents:
    right_ranked.appendChild(<ui:content content={c} />)
  page = \
  <ui:page title="Evan Stratford :: CV">
    {banner}
    <ui:two-columns>
      {left_ranked}
      {right_ranked}
    </ui:two-columns>
  </ui:page>
  return HttpResponse(page)
