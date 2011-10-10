from django.http import HttpResponse
from django.utils import simplejson

from cv.models import Tag, TagContentSimilarity

def json_response(request, json):
  callback = request.GET.get('callback')
  if callback is None:
    return HttpResponse(json, content_type='application/json')
  jsonp = '{0}({1})'.format(callback, json)
  return HttpResponse(jsonp, content_type='application/javascript')

def similar_content(request, tag_id):
  tag = Tag.objects.get(id=int(tag_id))
  similarity = TagContentSimilarity.objects.filter(tag=tag)
  similarity_map = {}
  for ts in similarity:
    similarity_map[ts.content_id] = ts.similarity
  json = simplejson.dumps(similarity_map)
  return json_response(request, json)
