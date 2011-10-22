from xhpy.pylib import *

class :ui:two-columns(:x:element):
  children :div, :div, :div
  def render(self):
    header, left, right = self.getChildren()
    return \
    <div class="UITwoColumns">
      <div class="UIHeader">
        {header}
      </div>
      <div class="UIColumns">
        <div class="UIColumn left">
          {left}
        </div>
        <div class="UIColumn right">
          {right}
        </div>
      </div>
    </div>
