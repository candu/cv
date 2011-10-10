from django.db import models

class BaseModel(models.Model):
  """
  Provides a default timestamping layer for Django models. This is useful in
  debugging DB issues, since you can see exactly when each piece of content
  was created/modified.
  """
  created_at = models.DateTimeField(auto_now_add=True)
  last_modified_at = models.DateTimeField(auto_now=True, auto_now_add=True)

  @classmethod
  def get_or_none(cls, *args, **kwargs):
    """
    Unlike get(), returns None if there are duplicate or zero rows for
    the given filter. For instance:
    """
    try:
      return cls.objects.get(*args, **kwargs)
    except (cls.DoesNotExist, cls.MultipleObjectsReturned):
      return None

  @classmethod
  def get_or_new(cls, *args, **kwargs):
    """
    Unlike get(), returns a new instance if there are zero rows.
    """
    try:
      return cls.objects.get(*args, **kwargs)
    except cls.DoesNotExist:
      return cls(*args, **kwargs)

  @classmethod
  def get_id_mapping(cls):
    """
    Returns a dict { id : instance }, where id is the row ID.
    """
    return dict((x.id, x) for x in cls.objects.all())

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
  """
  Tags are little semantic markers describing other pieces of this CV. They are
  primarily used for a sort of tag similarity filtering mechanism, enabling the
  viewer/reader to manipulate the CV. The timeline layout here is actually
  two-dimensional: vertical for time, horizontal for tag similarity based on
  whatever tags the user has selected.
  """
  path = models.CharField(max_length=255)
  title = models.CharField(max_length=255)

  def baseName(self):
    return self.path.split('/')[-1]

class Content(BaseModel):
  """
  Parent class for content types. Instead of having separate Activity, Event,
  and Era tables, this uses the contenttype column to decide what everything
  is.
  """
  # Content types

  tags = models.ManyToManyField(Tag, through='ContentTag')
  ACTIVITY = 'activity'
  ERA = 'era'
  EVENT = 'event'
  CONTENT_TYPE_CHOICES = (
      (ACTIVITY, ACTIVITY),
      (ERA, ERA),
      (EVENT, EVENT),
  )
  content_type = models.CharField(max_length=255, choices=CONTENT_TYPE_CHOICES)
  filename = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  description = models.TextField()
  started = models.DateField()
  finished = models.DateField(null=True, blank=True)

class ContentTag(BaseModel):
  """
  We use this to track which tags are autotags; we want non-autotags to
  persist across content updates, whereas autotags should be regenerated.
  """
  content = models.ForeignKey(Content)
  tag = models.ForeignKey(Tag)
  is_autotag = models.BooleanField(default=False)

class TagContentSimilarity(BaseModel):
  """
  Models precomputed tag-content similarity. In this application, we use
  the Expected Mutual Information Metric (EMIM), which determines similarity
  using generalized co-occurrence counts.
  """
  tag = models.ForeignKey(Tag, related_name='+')
  content = models.ForeignKey(Content, related_name='+')
  similarity = models.FloatField()
