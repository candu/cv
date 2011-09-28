from xhpy.pylib import *
from cv.lib.text_tagger import TextTagger
from cv.models import Activity, Tag
from cv.ui.tags import :ui:tag

import random
import re

class :ui:tagged-text(:x:element):
  children pcdata
  TAG_REGEX = re.compile(r'(\[@tag:[^\]]*\])')
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
  attribute Activity activity
  def render(self):
    activity = self.getAttribute('activity')
    return \
    <div class="UIActivity">
      <div class="UIActivityTitle">
        {activity.title}
      </div>
      <ui:tagged-text>
        {activity.blurb}
      </ui:tagged-text>
    </div>

class :ui:timeline(:x:element):
  attribute list activities
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
    for activity in self.getAttribute('activities'):
      timeline.appendChild(<ui:activity activity={activity} />)
    return timeline

