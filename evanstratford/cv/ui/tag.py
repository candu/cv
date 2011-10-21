from xhpy.pylib import *
from cv.models import Tag

class :ui:tag(:x:element):
  attribute Tag tag
  def render(self):
    tag = self.getAttribute('tag')
    tag_id = 'tag-{0}'.format(tag.id)
    return <a class={'UITag {0}'.format(tag_id)} title={tag.title}>{tag.name}</a>
