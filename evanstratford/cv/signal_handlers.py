from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from cv.lib.text_tagger import TextTagger
from cv.models import Activity

def autotag(activity):
  blurb_tags = TextTagger.getTags(activity.blurb)
  description_tags = TextTagger.getTags(activity.description)
  activity.tags = blurb_tags.union(description_tags)

@receiver(pre_save, sender=Activity)
def pre_save_activity(sender, instance, raw, using, *args, **kwargs):
  if instance.id is not None:
    # we can autotag here, since we have a primary key!
    autotag(instance)

@receiver(post_save, sender=Activity)
def post_save_activity(sender, instance, created, raw, using, *args, **kwargs):
  if created:
    # we have to autotag here instead, since we didn't have a primary key
    # in pre_save_activity!
    autotag(instance)
    instance.save()
