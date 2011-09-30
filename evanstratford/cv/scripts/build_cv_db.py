"""
build_cv_db.py

Usage:
  build_cv_db.py <content_dir>

Looks through

<content_dir>/activities
<content_dir>/eras
<content_dir>/events

for files containing data for objects of the corresponding types. The formats
are:

Activities/Eras
===============

<title>
<started> - <finished>
<tag>, ...

<description>

Events
======
<title>
<started> - <finished>
<tag>, ...

<blurb>

It then populates the database, including autotag extraction and tag similarity
calculations.
"""

import markdown
import os.path
import sys

from cv.lib.text_tagger import TextTagger
from cv.models import Activity, Era, Event, Tag, TagSimilarity

USAGE_MSG = """\
Usage:
  build_cv_db.py <content_dir>
"""

class ActivityParser(object):
  def parse(self, f):
    return [], None

class EraParser(object):
  def parse(self, f):
    return [], None

class EventParser(object):
  def parse(self, f):
    return [], None

class DatabaseBuilder(object):
  def __init__(self, content_dir, subdir_map):
    for subdir, parser_class in subdir_map.iteritems():
      parser = parser_class()
      content_subdir = os.path.join(content_dir, subdir)
      if not os.path.exists(content_subdir):
        print 'eek: {0}'.format(content_subdir)
      os.path.walk(content_subdir, self._visit, parser)

      self._buildSimilarityMap()

  def _visit(self, parser, dirname, names):
    print dirname, names
    for name in names:
      filename = os.path.join(dirname, name)
      with file(filename) as f:
        autotags, instance = parser.parse(f)
        #for tag in autotags:
        #  tag.save()
        #instance.save()

  def _buildSimilarityMap(self):
    # TODO: get all rows from cv_activitys_tags
    # TODO: crunch for EMIM
    # TODO: push back to DB
    pass

if __name__ == '__main__':
  def usage(msg):
    print USAGE_MSG
    print msg
    sys.exit(1)
  if len(sys.argv) < 2:
    usage('Not enough arguments.')
  content_dir = sys.argv[1]
  if not os.path.exists(content_dir):
    usage('Content directory {0} does not exist.'.format(content_dir))
  subdir_map = {
    'activities' : ActivityParser,
    'eras' : EraParser,
    'events' : EventParser,
  }
  DatabaseBuilder(content_dir, subdir_map)
