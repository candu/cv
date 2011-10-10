from xhpy.pylib import *

from cv.lib.date import date_now
from cv.lib.text_tagger import TextTagger
from cv.models import Content, Tag
from cv.ui.tags import :ui:tag

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
  attribute Content activity
  def render(self):
    activity = self.getAttribute('activity')
    today = date_now()
    time_delta = today - activity.finished
    time_duration = activity.finished - activity.started
    top = time_delta.days * self.PIXELS_PER_DAY
    min_height = time_duration.days * self.PIXELS_PER_DAY

    return \
        <div class="UIActivity" id={'activity-{0}'.format(activity.id)} style={'top: {0}px; min-height: {1}px'.format(top + 30, min_height)}>
      <div class="UIActivityTitle">
        {activity.title}
      </div>
    </div>

class :ui:timeline(:x:element):
  attribute list contents
  children :ui:activity*
  def render(self):
    timeline = \
    <div class="UITimeline">
      <div class="UITimelineHeader">
        <div class="UIHorizAxis">
          <div class="UIHorizAxisLeft"><div>work</div></div>
          <div class="UIHorizAxisRight"><div>play</div></div>
        </div>
      </div>
    </div>
    contents = self.getAttribute('contents')
    for content in contents:
      if content.content_type == Content.ACTIVITY:
        timeline.appendChild(<ui:activity activity={content} />)
    return timeline
