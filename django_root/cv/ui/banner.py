from xhpy.pylib import *

from cv.ui.img import :ui:img
from cv.ui.tag import :ui:tag

class :ui:banner(:x:element):
  attribute string name, list coordinates, list tags, list categories

  def _renderCoordinate(self, key, text, link):
    if link is not None:
      text = <a href={link}>{text}</a>
    return \
    <div class={'UICoord {0}'.format(key)}>
      <span class="UICoordIcon">
        <ui:img width={32} path={'{0}.png'.format(key)} />
      </span>
      <span class="UICoordText">{text}</span>
    </div>

  def _renderCategory(self, tag_map, category_name, category_tags, width):
    return \
    <div class="UICategory" style={'width: {0}%'.format(width)}>
      <div class="title">{category_name}</div>
      <div class="tags">
        {[<ui:tag tag={tag_map[tag_name]} /> for tag_name in category_tags]}
      </div>
    </div>

  def _renderTagBlock(self):
    tag_map = dict((tag.name, tag) for tag in self.getAttribute('tags'))
    categories = self.getAttribute('categories')
    width = 100 / len(categories)
    category_div = \
    <div class="UICategories">
      {[self._renderCategory(tag_map, name, tags, width) for name, tags in categories]}
    </div>

    return \
    <div class="UITagBlock">
      <div class="description">
        View the parts most relevant to you by using these tags to filter my CV.
      </div>
      {category_div}
    </div>


  def render(self):
    coordinates = self.getAttribute('coordinates')
    coords_div = \
    <div class="UICoordinates segment">
      <div class="title">Coordinates</div>
      <div class="description">
        {[self._renderCoordinate(key, text, link) for key, text, link in coordinates]}
      </div>
    </div>

    mission = \
    <div class="UIMission segment">
      <div class="title">Mission</div>
      <div class="description">
        To{' '}<em>solve problems</em>,{' '}<em>crunch data</em>,
        and{' '}<em>build systems</em>{' '}that impact real people.
      </div>
    </div>

    name = self.getAttribute('name')
    return \
    <div class="UIBanner">
      <div class="UIName">{name}</div>
      <div class="UISegments">
        {coords_div}
        {mission}
      </div>
      {self._renderTagBlock()}
    </div>
