from xhpy.pylib import *

class :ui:page(:x:element):
  attribute string title
  def render(self):
    title = self.getAttribute('title')
    head = \
    <head>
      <title>{title}</title>
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
