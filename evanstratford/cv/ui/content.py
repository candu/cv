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

class :ui:content(:x:element):
  DATE_FORMAT = '%b %e, %Y'
  attribute Content content
  def render(self):
    content = self.getAttribute('content')
    content_id = 'content-{0}'.format(content.id)
    content_tags = <div class="UIContentTags" />
    for tag in content.tags.all():
      content_tags.appendChild(<ui:tag tag={tag} />)
    content_date = content.finished.strftime(self.DATE_FORMAT)
    if content.started is not None:
      content_date = '{0} to {1}'.format(
          content.started.strftime(self.DATE_FORMAT),
          content_date)
    return \
    <div class="UIContent" id={content_id}>
      <div class="UIContentHeader">
        {content_tags}
        <div class="UIContentTitle">
          {content.title}
        </div>
        <div class="UIContentDate">
          {content_date}
        </div>
      </div>
      <div class="UIContentDescription">
        <text>
          {content.description}
        </text>
      </div>
      <div class="UIContentMoreLess">
        Show more...
      </div>
    </div>
