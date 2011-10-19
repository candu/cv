from django.utils import simplejson

from cv.lib.json import json_response
from cv.models import Tag, TagContentSimilarity

def similar_content(request, tag_id):
  tag = Tag.objects.get(id=int(tag_id))
  similarity = TagContentSimilarity.objects.filter(tag=tag)
  similarity_map = {}
  for ts in similarity:
    similarity_map[ts.content_id] = ts.similarity
  json = simplejson.dumps({
    'tag': {
      'id': tag.id,
      'path': tag.path,
      'title': tag.title,
    },
    'similarity': similarity_map,
  })
  return json_response(request, json)

def tags(request):
  mapping = dict((tag.path, tag.id) for tag in Tag.objects.all())
  json = simplejson.dumps(mapping)
  return json_response(request, json)
