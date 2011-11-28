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
  name = models.CharField(max_length=255)
  title = models.CharField(max_length=255)

class Content(BaseModel):
  tags = models.ManyToManyField(Tag)
  filename = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  org = models.CharField(max_length=255)
  description = models.TextField()
  started = models.DateField(null=True, blank=True)
  finished = models.DateField()
