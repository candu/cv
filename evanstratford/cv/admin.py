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
  list_display = ('name',
                  'id', 'title')
  search_fields = ['name', 'title']
  ordering = ['name']

class ContentAdmin(AdminBase):
  fieldsets = [
    (None, {'fields' : ['title', 'description']}),
    ('Duration', {'fields' : ['started', 'finished']}),
  ]
  list_display = ('title',
                  'id', 'filename', 'started', 'finished')
  search_fields = ['title', 'description']
  ordering = ['-started', '-finished']

admin.site.register(Content, ContentAdmin)
admin.site.register(Tag, TagAdmin)
