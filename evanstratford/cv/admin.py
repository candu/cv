from cv.models import Tag, Activity
from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
  list_display = ('path', 'description')
  search_fields = ['path']

class ActivityAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields' : ['description']}),
    ('Duration', {'fields' : ['started', 'finished']}),
    ('Associations', {'fields' : ['parent', 'tags']}),
  ]
  list_display = ('description', 'parent_description', 'started', 'finished')
  list_filter = ['started', 'finished']
  search_fields = ['description']

admin.site.register(Tag, TagAdmin)
admin.site.register(Activity, ActivityAdmin)
