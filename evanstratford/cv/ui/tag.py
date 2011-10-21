from xhpy.pylib import *
from cv.models import Tag

class :ui:tag(:x:element):
  attribute Tag tag
  def render(self):
    tag = self.getAttribute('tag')
    return <a class="UITag" title={tag.title}>{tag.name}</a>
