from django.http import HttpResponse
from django.utils import simplejson

from cv.models import Tag, TagSimilarity

def json_response(request, json):
  print 'foo'
  callback = request.GET.get('callback')
  if callback is None:
    return HttpResponse(json, content_type='application/json')
  jsonp = '{0}({1})'.format(callback, json)
  return HttpResponse(jsonp, content_type='application/javascript')

def similar_tags(request, tag_id):
  tag = Tag.objects.get(id=int(tag_id))
  json = simplejson.dumps({
    'foo' : 42
  })
  return json_response(request, json)
