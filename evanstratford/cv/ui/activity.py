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

class :text(:x:primitive):
  children pcdata
  category %flow
  def stringify(self):
    text = self.getChildren()[0]
    return text

class :ui:activity(:x:element):
  attribute Content activity
  def render(self):
    activity = self.getAttribute('activity')
    activity_id = 'activity-{0}'.format(activity.id)
    return \
    <div class="UIActivity" id={activity_id}>
      <div class="UIActivityTitle">
        {activity.title}
      </div>
      <div class="UIActivityDescription">
        <text>
          {activity.description}
        </text>
      </div>
    </div>
