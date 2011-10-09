from cv.models import Content, Tag
from django import forms
from django.contrib import admin

class AdminMedia(object):
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    '/static/admin/js/editor.js',
  )
  css = {
    'all': ('/static/admin/css/editor.css',),
  }

class AdminBase(admin.ModelAdmin):
  Media = AdminMedia

class TagAdmin(AdminBase):
  list_display = ('path', 'title')
  search_fields = ['path', 'title']
  ordering = ['path']

class ContentAdmin(AdminBase):
  fieldsets = [
    (None, {'fields' : ['content_type', 'title', 'description']}),
    ('Duration', {'fields' : ['started', 'finished']}),
  ]
  list_display = ('content_type', 'filename', 'title', 'started', 'finished')
  search_fields = ['title', 'description']
  ordering = ['-started', '-finished']

admin.site.register(Content, ContentAdmin)
admin.site.register(Tag, TagAdmin)
