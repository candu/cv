from xhpy.pylib import *

from cv.lib.date import date_now
from cv.lib.text_tagger import TextTagger
from cv.models import Content, Tag
from cv.ui.tag import :ui:tag

import datetime
import random

class :ui:tagged-text(:x:element):
  children pcdata
  def render(self):
    text = self.getFirstChild()
    tagged_text = <div class="UITaggedText" />
    for part in TextTagger.tag(text):
      if isinstance(part, Tag):
        tagged_text.appendChild(<ui:tag tag={tag} />)
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
  DATE_FORMAT = '%b %e, %Y'
  attribute Content activity
  def render(self):
    activity = self.getAttribute('activity')
    activity_id = 'activity-{0}'.format(activity.id)
    activity_tags = <div class="UIActivityTags" />
    for tag in activity.tags.all():
      activity_tags.appendChild(<ui:tag tag={tag} />)
    activity_date = activity.finished.strftime(self.DATE_FORMAT)
    if activity.started is not None:
      activity_date = '{0} to {1}'.format(
          activity.started.strftime(self.DATE_FORMAT),
          activity_date)
    return \
    <div class="UIActivity" id={activity_id}>
      <div class="UIActivityHeader">
        {activity_tags}
        <div class="UIActivityTitle">
          {activity.title}
        </div>
        <div class="UIActivityDate">
          {activity_date}
        </div>
      </div>
      <div class="UIActivityDescription">
        <text>
          {activity.description}
        </text>
      </div>
    </div>
