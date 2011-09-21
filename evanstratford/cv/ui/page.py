from django.conf import settings
from xhpy.pylib import *

class :ui:page(:x:element):
  attribute string title
  def render(self):
    title = self.getAttribute('title')
    head = \
    <head>
      <title>{title}</title>
      <script src={settings.STATIC_URL + 'js/mootools.js'}></script>
      <script src={settings.STATIC_URL + 'js/cv.js'}></script>
      <link href={settings.STATIC_URL + 'css/cv.css'} rel="stylesheet" type="text/css" />
    </head>
    body = <body/>
    for child in self.getChildren():
      body.appendChild(child)
    return \
    <x:doctype>
      <html>
        {head}
        {body}
      </html>
    </x:doctype>
