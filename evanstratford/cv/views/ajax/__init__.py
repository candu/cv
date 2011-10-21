from django.utils import simplejson

from cv.lib.json import json_response
from cv.models import Tag

def tags(request):
  mapping = dict((tag.path, tag.id) for tag in Tag.objects.all())
  json = simplejson.dumps(mapping)
  return json_response(request, json)
