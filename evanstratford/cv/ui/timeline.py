from xhpy.pylib import *

from cv.lib.date import date_now
from cv.lib.text_tagger import TextTagger
from cv.models import Content, Tag
from cv.ui.tags import :ui:tag
from cv.ui.typeahead import :ui:typeahead

import datetime

class :ui:tagged-text(:x:element):
  children pcdata
  def render(self):
    text = self.getFirstChild()
    tagged_text = <div class="UITaggedText" />
    for part in TextTagger.tag(text):
      if isinstance(part, Tag):
        tag_data = (part.baseName(), part.description)
        tagged_text.appendChild(<ui:tag tag-data={tag_data} />)
      else:
        tagged_text.appendChild(part)
    return tagged_text

class :ui:activity(:x:element):
  PIXELS_PER_DAY = 2
  PIXELS_FROM_TOP = 30
  attribute Content activity
  def render(self):
    activity = self.getAttribute('activity')
    activity_id = 'activity-{0}'.format(activity.id)
    return \
    <div class="UIActivity" id={activity_id}>
      <div class="UIActivityTitle">
        {activity.title}
      </div>
    </div>

class :ui:timeline-header(:x:element):
  def render(self):
    return \
    <div class="UITimelineHeader">
      <div class="UIHorizAxis">
        <div class="UIHorizAxisLeft">
          <ui:typeahead />
        </div>
        <div class="UIHorizAxisRight">
          <ui:typeahead />
        </div>
      </div>
    </div>

class :ui:timeline(:x:element):
  attribute list contents
  children :ui:activity*
  def render(self):
    timeline = \
    <div class="UITimeline">
      <ui:timeline-header />
    </div>
    contents = self.getAttribute('contents')
    activities = sorted(
        [c for c in contents if c.content_type == Content.ACTIVITY],
        key=lambda c: c.finished,
        reverse=True)
    for activity in activities:
      timeline.appendChild(<ui:activity activity={activity} />)
    return timeline
