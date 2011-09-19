from cv.models import Tag, Activity
from django.contrib import admin

class ActivityAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields' : ['description']}),
    ('Duration', {'fields' : ['started', 'finished']}),
    ('Associations', {'fields' : ['parent', 'tags']}),
  ]

admin.site.register(Tag)
admin.site.register(Activity, ActivityAdmin)
