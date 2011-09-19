from django.db import models

class Tag(models.Model):
  path = models.CharField(max_length=255)
  description = models.CharField(max_length=255)

class Activity(models.Model):
  tags = models.ManyToManyField(Tag)
  sub_activities = models.ForeignKey('self')
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  started = models.DateTimeField()
  finished = models.DateTimeField()
