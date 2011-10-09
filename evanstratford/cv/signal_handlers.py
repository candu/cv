from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from cv.lib.text_tagger import TextTagger
from cv.models import Content, Event

def autotag_content(content):
  blurb_tags = TextTagger.getTags(content.blurb)
  description_tags = TextTagger.getTags(content.description)
  content.tags = blurb_tags.union(description_tags)

def autotag_event(event):
  event.tags = TextTagger.getTags(event.blurb)

@receiver(pre_save, sender=Content)
def pre_save_content(sender, instance, raw, using, *args, **kwargs):
  if instance.id is not None:
    # we can autotag here, since we have a primary key!
    autotag_content(instance)

@receiver(post_save, sender=Content)
def post_save_content(sender, instance, created, raw, using, *args, **kwargs):
  if created:
    # we have to autotag here instead, since we didn't have a primary key
    # in pre_save_content!
    autotag_content(instance)
    instance.save()
