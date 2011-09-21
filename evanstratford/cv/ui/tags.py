from xhpy.pylib import *
from cv.models import Tag

class :ui:tag(:li):
  attribute Tag tag
  def render(self):
    return <li>{tag.path}</li>

class :ui:tags(:x:element):
  attribute list tags
  def render(self):
    tag_list = <ul class="UITagList"/>
    for tag in tags:
      tag_list.append(<ui:tag tag={tag} />)
    return tag_list

