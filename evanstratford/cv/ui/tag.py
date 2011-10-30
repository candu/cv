from xhpy.pylib import *
from cv.models import Tag

class :ui:tag(:x:element):
  attribute Tag tag
  def render(self):
    tag = self.getAttribute('tag')
    tag_id = 'tag-{0}'.format(tag.id)
    tag_class = 'UITag {0}'.format(tag_id)
    return <a class={tag_class} title={tag.title}>{tag.name}</a>
