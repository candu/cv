from django.db import models

class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  last_modified_at = models.DateTimeField(auto_now=True, auto_now_add=True)

  def __unicode__(self):
    """
    Provides an easy way to see the state of a BaseModel object via
    BaseModelSubClass.objects.all(); objects listed there are printed with
    all available column data, which is fetched by introspecting __dict__
    here.
    """
    field_info = u', '.join(
        u'{0}={1}'.format(attr, unicode(str(val), 'utf-8'))
        for attr, val in sorted(self.__dict__.items()) if attr != '_state')
    return u'{0}({1})'.format(self.__class__.__name__, field_info)

  class Meta:
    abstract = True

class Tag(BaseModel):
  path = models.CharField(max_length=255)
  description = models.CharField(max_length=255)

class Activity(BaseModel):
  tags = models.ManyToManyField(Tag)
  parent = models.ForeignKey('self', blank=True, null=True)
  description = models.CharField(max_length=255)
  started = models.DateField()
  finished = models.DateField()

  def parent_description(self):
    if self.parent is None:
      return None
    return self.parent.description
  parent_description.short_description = 'Parent Description'
