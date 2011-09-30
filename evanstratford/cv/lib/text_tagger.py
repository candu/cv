from cv.models import Tag
import re

class InvalidTagSlugException(Exception):
  def __init__(self, slug):
    super(Exception, self).__init__("""\
Invalid tag slug

%s""" % slug)

class TextTagger(object):
  TAG_REGEX = re.compile(r'(\[@tag:[^\]]*\])')

  @classmethod
  def tag(cls, text):
    tagged_parts = []
    for part in re.split(cls.TAG_REGEX, text):
      if re.match(cls.TAG_REGEX, part):
        path = part[6:-1]
        tag = Tag.objects.get(path=path)
        if tag is None:
          raise InvalidTagSlugException(part)
        tagged_parts.append(tag)
      else:
        tagged_parts.append(part)
    return tagged_parts

  @classmethod
  def getTags(cls, text):
    return set([part for part in cls.tag(text) if isinstance(part, Tag)])
