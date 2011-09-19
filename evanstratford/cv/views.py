from django.http import HttpResponse
from xhpy.pylib import *
from cv.ui.foo import :ui:foo

def index(request):
  response = <div class="baz"><ui:foo bar={range(3)} /></div>
  return HttpResponse(str(response))
