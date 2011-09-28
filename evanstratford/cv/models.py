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

  def baseName(self):
    return tag.path.split('/')[-1]

class TagSimilarity(BaseModel):
  """
  Models a precomputed similarity metric on tags. In this application, we use
  the Expected Mutual Information Metric (EMIM), which determines similarity
  using generalized co-occurrence counts.
  """
  tag1 = models.ForeignKey(Tag, related_name='+')
  tag2 = models.ForeignKey(Tag, related_name='+')
  similarity = models.FloatField()

class Activity(BaseModel):
  tags = models.ManyToManyField(Tag)
  title = models.CharField(max_length=255)
  blurb = models.CharField(max_length=255)
  description = models.TextField()
  started = models.DateField()
  finished = models.DateField()
