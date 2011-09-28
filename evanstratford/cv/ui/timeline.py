from xhpy.pylib import *

from cv.lib.text_tagger import TextTagger
from cv.models import Activity, Tag
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
  attribute Activity activity,
            datetime.date last-activity-time
  def render(self):
    activity = self.getAttribute('activity')
    last_activity_time = self.getAttribute('last-activity-time')
    time_delta = last_activity_time - activity.finished
    time_duration = activity.finished - activity.started
    top = time_delta.days * self.PIXELS_PER_DAY
    min_height = time_duration.days * self.PIXELS_PER_DAY

    return \
        <div class="UIActivity" id={'activity-{0}'.format(activity.id)} style={'top: {0}px; min-height: {1}px'.format(top + 30, min_height)}>
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
    activities = self.getAttribute('activities')
    last_activity_time = max(a.finished for a in activities)
    for activity in activities:
      timeline.appendChild(
          <ui:activity activity={activity}
                       last-activity-time={last_activity_time}/>)
    return timeline

