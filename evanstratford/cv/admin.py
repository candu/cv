from cv.models import Tag, Activity
from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
  list_display = ('path', 'description')
  search_fields = ['path']

class ActivityAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields' : ['title', 'blurb', 'description']}),
    ('Duration', {'fields' : ['started', 'finished']}),
  ]
  list_display = ('title', 'blurb', 'started', 'finished')
  list_filter = ['started', 'finished']
  search_fields = ['title', 'blurb', 'description']

admin.site.register(Tag, TagAdmin)
admin.site.register(Activity, ActivityAdmin)
