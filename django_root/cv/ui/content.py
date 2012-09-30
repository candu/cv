from xhpy.pylib import *

from cv.lib.date import date_now
from cv.models import Content, Tag
from cv.ui.tag import :ui:tag

import datetime
import random

class :text(:x:primitive):
  children pcdata
  category %flow
  def stringify(self):
    text = self.getChildren()[0]
    return text

class :ui:content(:x:element):
  DATE_FORMAT = '%b %e, %Y'
  attribute Content content
  def _renderDates(self, started, finished):
    started_date = started.strftime(self.DATE_FORMAT)
    if not finished:
      finished_date = 'present'
    else:
      finished_date = finished.strftime(self.DATE_FORMAT)
    if started_date == finished_date:
      return started_date
    return '{0} to {1}'.format(started_date, finished_date)

  def render(self):
    content = self.getAttribute('content')
    content_tags = <div class="UIContentTags" />
    for tag in sorted(content.tags.all(), key=lambda t: t.name):
      content_tags.appendChild(<ui:tag tag={tag} />)
    content_date = self._renderDates(content.started, content.finished)
    content_org = None
    if content.org:
      content_org = \
      <div class="UIContentOrg">
        {content.org}
      </div>
    return \
    <div class="UIContent" id={content.filename}>
      <div class="UIContentHeader">
        {content_tags}
        <div class="UIContentTitle">
          {content.title}
        </div>
        {content_org}
        <div class="UIContentDate">
          {content_date}
        </div>
      </div>
      <div class="UIContentDescription">
        <text>
          {content.description}
        </text>
      </div>
    </div>
