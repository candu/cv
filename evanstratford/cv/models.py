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
  """
  Tags are little semantic markers describing other pieces of this CV. They are
  primarily used for a sort of tag similarity filtering mechanism, enabling the
  viewer/reader to manipulate the CV. The timeline layout here is actually
  two-dimensional: vertical for time, horizontal for tag similarity based on
  whatever tags the user has selected.
  """
  path = models.CharField(max_length=255)
  description = models.CharField(max_length=255)

  def baseName(self):
    return self.path.split('/')[-1]

class TagSimilarity(BaseModel):
  """
  Models a precomputed similarity metric on tags. In this application, we use
  the Expected Mutual Information Metric (EMIM), which determines similarity
  using generalized co-occurrence counts.
  """
  tag1 = models.ForeignKey(Tag, related_name='+')
  tag2 = models.ForeignKey(Tag, related_name='+')
  similarity = models.FloatField()

class Event(BaseModel):
  """
  An event is something of interest that took place at a particular point in
  time. These include awards, specific birthdays, hackathons, etc. The primary
  reason for separating these from activities is presentational: these are
  best represented as points with small blurbs, whereas activities are best
  represented as blocks with longer descriptions.

  Events don't have longer descriptions - they only have shorter blurbs.
  """
  tags = models.ManyToManyField(Tag)
  title = models.CharField(max_length=255)
  blurb = models.CharField(max_length=255)
  happened_at = models.DateField()

class Activity(BaseModel):
  """
  An activity is something of interest that took place over a longer duration;
  jobs, volunteer positions, and longer projects fit the bill here. See Event
  class for the description of how these are different.
  """
  tags = models.ManyToManyField(Tag)
  title = models.CharField(max_length=255)
  blurb = models.CharField(max_length=255)
  description = models.TextField()
  started = models.DateField()
  finished = models.DateField()

class Era(BaseModel):
  """
  An era is a period in my life that I consider consistent or self-contained in
  some manner. High school, university, the bike trip, and my full-time work
  life all fit into this category - they aren't really activities, since they
  don't highlight achievements or experiences directly, but they are useful
  groupings.

  Eras don't have tags; they are intended as longer narratives, providing a
  bit of backstory to the CV. They also lack short blurbs.
  """
  title = models.CharField(max_length=255)
  description = models.TextField()
  started = models.DateField()
  finished = models.DateField()
