from xhpy.pylib import *

from django.conf import settings

class :ui:img(:x:element):
    attribute string path, string width
    def render(self):
        path = self.getAttribute('path')
        width = self.getAttribute('width')
        return <img width={width} src={settings.STATIC_URL + 'img/' + path} />
