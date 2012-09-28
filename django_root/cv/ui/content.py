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
  def render(self):
    content = self.getAttribute('content')
    content_id = 'content-{0}'.format(content.id)
    content_tags = <div class="UIContentTags" />
    for tag in sorted(content.tags.all(), key=lambda t: t.name):
      content_tags.appendChild(<ui:tag tag={tag} />)
    content_date = content.finished.strftime(self.DATE_FORMAT)
    if content.started != content.finished:
      content_date = '{0} to {1}'.format(
          content.started.strftime(self.DATE_FORMAT),
          content_date)
    content_org = None
    if content.org:
      content_org = \
      <div class="UIContentOrg">
        {content.org}
      </div>
    return \
    <div class="UIContent" id={content_id}>
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
