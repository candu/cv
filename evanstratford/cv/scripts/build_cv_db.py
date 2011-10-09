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

import datetime
import dateutil.parser
import logging
import markdown
import os.path
import re
import sys

from cv.lib.text_tagger import TextTagger
from cv.models import Content, Tag, TagSimilarity

USAGE_MSG = """\
Usage:
  build_cv_db.py <content_dir>
"""

logging.basicConfig(level=logging.INFO)

def datetime_to_date(dt):
  return datetime.date(dt.year, dt.month, dt.day)

class ContentParserException(Exception):
  pass

class ContentParser(object):
  def parse(self, content_dir, filename, content_type):
    with open(filename) as f:
      title = f.readline().strip()
      dates = [date.strip() for date in f.readline().split('to')]
      print filename, dates
      if len(dates) == 0:
        raise ContentParserException('No dates specified')
      started = datetime_to_date(dateutil.parser.parse(dates[0]))
      finished = None
      if content_type != Content.EVENT:
        if len(dates) == 1:
          raise ContentParserException('Activities and Eras require two dates')
        if dates[1] == 'now':
          dt = datetime.datetime.now()
          finished = datetime.date(dt.year, dt.month, dt.day)
        else:
          finished = datetime_to_date(dateutil.parser.parse(dates[1]))
      paths = [path.strip() for path in f.readline().split(',')]
      tags = [Tag.objects.get_or_create(path=path) for path in paths]
      description = markdown.markdown(f.read())
    content = Content(
        content_type=content_type,
        filename=os.path.relpath(filename, content_dir),
        title=title,
        description=description,
        started=started,
        finished=finished)
    content.save()
    # TODO: deal with tags

class DatabaseBuilder(object):
  def __init__(self, content_dir, subdir_map):
    logging.info('populating database with content from {0}...'.format(
        content_dir))
    parser = ContentParser()
    for subdir, content_type in subdir_map.iteritems():
      content_subdir = os.path.join(content_dir, subdir)
      if not os.path.exists(content_subdir):
        print 'eek: {0}'.format(content_subdir)
      arg = (content_dir, content_type, parser)
      os.path.walk(content_subdir, self._visit, arg)

    logging.info('building tag similarity mapping...')
    self._buildSimilarityMap()

  def _visit(self, arg, dirname, names):
    content_dir, content_type, parser = arg
    parser = ContentParser()
    for name in names:
      filename = os.path.join(dirname, name)
      logging.info('parsing {0}: content_type == {1}...'.format(
          filename, content_type))
      parser.parse(content_dir, filename, content_type)

  def _buildSimilarityMap(self):
    # TODO: get all rows from cv_content_tags (or whatever)
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
    'activities' : Content.ACTIVITY,
    'eras' : Content.ERA,
    'events' : Content.EVENT,
  }
  DatabaseBuilder(content_dir, subdir_map)
