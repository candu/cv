from xhpy.pylib import *

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

class :ui:content(:x:element):
  PIXELS_PER_DAY = 2
  attribute Activity activity,
            datetime.date last-activity-time
  def render(self):
    content = self.getAttribute('content')
    last_content_time = self.getAttribute('last-content-time')
    time_delta = last_content_time - content.finished
    time_duration = content.finished - content.started
    top = time_delta.days * self.PIXELS_PER_DAY
    min_height = time_duration.days * self.PIXELS_PER_DAY

    return \
        <div class="UIContent" id={'content-{0}'.format(content.id)} style={'top: {0}px; min-height: {1}px'.format(top + 30, min_height)}>
      <div class="UIContentTitle">
        {content.title}
      </div>
    </div>

class :ui:timeline(:x:element):
  attribute list contents
  children :ui:content*
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
    last_content_time = max(c.finished for c in contents)
    for content in contents:
      timeline.appendChild(
          <ui:content content={content}
                      last-content-time={last_content_time}/>)
    return timeline
