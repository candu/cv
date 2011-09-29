from cv.models import Activity, Era, Event, Tag
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
  search_fields = ['title', 'blurb', 'description']

class EventAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields' : ['title', 'blurb']}),
    ('Time', {'fields' : ['happened_at']}),
  ]
  list_display = ('title', 'blurb', 'happened_at')
  search_fields = ['title', 'blurb']

class EraAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields' : ['title', 'description']}),
    ('Duration', {'fields' : ['started', 'finished']}),
  ]
  list_display = ('title', 'started', 'finished')
  search_fields = ['title', 'description']

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Era, EraAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Tag, TagAdmin)
