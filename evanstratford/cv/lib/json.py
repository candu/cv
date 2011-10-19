from django.http import HttpResponse

def json_response(request, json):
  callback = request.GET.get('callback')
  if callback is None:
    return HttpResponse(json, content_type='application/json')
  jsonp = '{0}({1})'.format(callback, json)
  return HttpResponse(jsonp, content_type='application/javascript')
