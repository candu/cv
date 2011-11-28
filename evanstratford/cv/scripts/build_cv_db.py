"""
build_cv_db.py

Usage:
  build_cv_db.py <content_dir>

Looks through <content_dir> for files containing content data. The file
format is:

<title>
[<started> to ]<finished>
<tag>, ...

<description>
"""

import datetime
import dateutil.parser
import logging
import markdown
import os.path
import sys

from cv.lib.text_tagger import TextTagger
from cv.models import Content, Tag

USAGE_MSG = __doc__

logging.basicConfig(level=logging.INFO)

def datetime_to_date(dt):
  return datetime.date(dt.year, dt.month, dt.day)

class ContentParserException(Exception):
  pass

class ContentParser(object):
  def parse(self, content_dir, filename):
    with open(filename) as f:
      title = f.readline().strip()
      dates = [date.strip() for date in f.readline().split('to')]
      if len(dates) == 0:
        raise ContentParserException('No dates specified')
      if len(dates) == 1:
        started = None
        finished = datetime_to_date(dateutil.parser.parse(dates[0]))
      else:
        started = datetime_to_date(dateutil.parser.parse(dates[0]))
        if dates[1] == 'now':
          finished = datetime_to_date(datetime.datetime.now())
        else:
          finished = datetime_to_date(dateutil.parser.parse(dates[1]))
      org = f.readline().strip()
      names = [name.strip() for name in f.readline().split(',')]
      tags = []
      for name in names:
        tag, created = Tag.objects.get_or_create(name=name)
        tags.append(tag)
      description = markdown.markdown(f.read())

    filename_relative = os.path.relpath(filename, content_dir)
    content = Content.get_or_new(filename=filename_relative)
    content.title = title
    content.org = org
    content.description = description
    content.started = started
    content.finished = finished
    content.save()

    for tag in tags:
      content.tags.add(tag)
    content.save()

class DatabaseBuilder(object):
  def __init__(self, content_dir):
    logging.info('populating database with content from {0}...'.format(
        content_dir))
    parser = ContentParser()
    arg = (content_dir, parser)
    os.path.walk(content_dir, self._visit, arg)

  def _visit(self, arg, dirname, names):
    content_dir, parser = arg
    for name in names:
      if name.endswith('.swp'):
        continue
      filename = os.path.join(dirname, name)
      logging.info('parsing {0}...'.format(filename))
      parser.parse(content_dir, filename)

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
  DatabaseBuilder(content_dir)
