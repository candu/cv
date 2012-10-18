from django.conf import settings
from xhpy.pylib import *

class :ui:page(:x:element):
  attribute string title
  def render(self):
    title = self.getAttribute('title')
    head = \
    <head>
      <meta name="google-site-verification" content="_g7MZQkAImP6eLTng2Uxim5mUW41jYJ1aZMaGDbm8aI" />
      <title>{title}</title>
      <script src={settings.STATIC_URL + 'js/mootools.js'}></script>
      <script src={settings.STATIC_URL + 'js/mootools-more.js'}></script>
      <script src={settings.STATIC_URL + 'js/mootools.history.js'}></script>
      <script src={settings.STATIC_URL + 'js/cv.js'}></script>
      <link href={settings.STATIC_URL + 'css/base.css'} rel="stylesheet" type="text/css" media="screen, print" />
      <link href={settings.STATIC_URL + 'css/cv.css'} rel="stylesheet" type="text/css" media="screen" />
      <link href={settings.STATIC_URL + 'css/cv-print.css'} rel="stylesheet" type="text/css" media="print" />
      <script src={settings.STATIC_URL + 'js/ga.js'}></script>
    </head>
    container = <div id="container" />
    for child in self.getChildren():
      container.appendChild(child)
    return \
    <x:doctype>
      <html>
        {head}
        <body>
          {container}
        </body>
      </html>
    </x:doctype>
