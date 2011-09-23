from xhpy.pylib import *
from cv.models import Tag

class :ui:tag(:x:element):
  attribute tuple tag-data
  def render(self):
    path, description = self.getAttribute('tag-data')
    return <a class="UITag enabled" href="#" title={description}>{path}</a>

class :ui:tag-group(:x:element):
  attribute string group-name, list tag-data
  children (:ui:tag | :ui:tag-group)*
  def render(self):
    group_name = self.getAttribute('group-name')
    group_list = \
    <div class="UITagGroup">
      <div class="UITagGroupName">{group_name}</div>
    </div>
    tags = []
    groups = {}
    for path, description in self.getAttribute('tag-data'):
      path_parts = path.split('/')
      if len(path_parts) == 1:
        tags.append((path, description))
        continue
      group = path_parts[0]
      subpath = '/'.join(path_parts[1:])
      group_tag_data = groups.setdefault(group, [])
      group_tag_data.append((subpath, description))
    for path, description in sorted(tags):
      group_list.appendChild(<ui:tag tag-data={(path, description)} />)
    for group, group_tag_data in sorted(groups.iteritems()):
      group_list.appendChild(
          <ui:tag-group group-name={group} tag-data={group_tag_data} />)
    return group_list

class :ui:tags(:x:element):
  attribute list tags
  children (:ui:tag | :ui:tag-group)*
  def render(self):
    tag_data = []
    for tag in self.getAttribute('tags'):
      if not tag.path.startswith('/'):
        raise Exception('invalid tag path {0}'.format(tag.path))
      tag_data.append((tag.path[1:], tag.description))
    return <ui:tag-group group-name="/" tag-data={tag_data} />
