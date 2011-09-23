from xhpy.pylib import *

class :ui:two-column-layout(:x:element):
  children :x:element, :x:element
  def render(self):
    left, right = self.getChildren()
    return \
    <div class="UITwoColumnLayout">
      <div class="UISidebar">
        {left}
      </div>
      <div class="UIContentContainer">
        <div class="UIContent">
          {right}
        </div>
      </div>
    </div>
