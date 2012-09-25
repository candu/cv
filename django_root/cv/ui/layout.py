from xhpy.pylib import *

class :ui:two-columns(:x:element):
  children :div, :div
  def render(self):
    left, right = self.getChildren()
    return \
    <div class="UITwoColumns">
      <div class="UIColumns">
        <div class="UIColumn left">
          {left}
        </div>
        <div class="UIColumn right">
          {right}
        </div>
      </div>
    </div>
