from xhpy.pylib import *
from cv.models import Activity
from cv.ui.tags import :ui:tag

class :ui:activity(:x:element):
  attribute Activity activity
  def render(self):
    return

class :ui:timeline(:x:element):
  attribute list activities
  children :ui:activity*
  def render(self):
    return <div>{'the ' * 10000}</div>
