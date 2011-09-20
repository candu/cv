from django.http import HttpResponse
from xhpy.pylib import *
from cv.ui.page import :ui:page

def index(request):
  content = <div class="baz"><ul><li>foo</li></ul></div>
  page = <ui:page title="Evan Stratford :: CV">{content}</ui:page>
  return HttpResponse(page)
