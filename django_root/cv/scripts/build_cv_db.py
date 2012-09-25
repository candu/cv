"""
build_cv_db.py

Usage:
  build_cv_db.py <content_dir>

Looks through <content_dir> for files containing content data. This uses a
Jekyll-style YAML-front-matter-plus-Markdown approach.
"""

import datetime
import dateutil.parser
import logging
import markdown
import os.path
import sys
import yaml

from cv.lib.text_tagger import TextTagger
from cv.models import Content, Tag

USAGE_MSG = __doc__

logging.basicConfig(level=logging.INFO)

def string_to_date(s):
  return datetime_to_date(dateutil.parser.parse(s))

def datetime_to_date(dt):
  return datetime.date(dt.year, dt.month, dt.day)

class ContentParserException(Exception):
  pass

class ContentParser(object):
  def _readFrontMatter(self, f):
    line = f.readline()
    if not line.startswith('---'):
      raise ContentParserException('Expected front matter begin')
    front_matter = []
    while True:
      line = f.readline()
      if not line:
        raise ContentParserException('Expected front matter end')
      if line.startswith('---'):
        break
      front_matter.append(line)
    return yaml.load(''.join(front_matter))

  def _readDescription(self, f):
    return markdown.markdown(f.read())

  def _getDates(self, front_matter):
    from_str = front_matter.get('from')
    if not from_str:
      raise ContentParserException('Expected (from, to) dates')
    to_str = front_matter.get('to')
    if not to_str:
      raise ContentParserException('Expected (from, to) dates')
    started = string_to_date(from_str)
    if to_str in ['now', 'current', 'present']:
      finished = datetime_to_date(datetime.datetime.now())
    else:
      finished = string_to_date(to_str)
    return (started, finished)

  def parse(self, content_dir, filename):
    with open(filename) as f:
      front_matter = self._readFrontMatter(f)
      description = self._readDescription(f)

    filename_relative = os.path.relpath(filename, content_dir)
    content = Content.get_or_new(filename=filename_relative)
    content.title = front_matter['title']
    content.started, content.finished = self._getDates(front_matter)
    content.org = front_matter.get('org', '')
    tags = []
    for tag_name in front_matter['tags']:
      tag, created = Tag.objects.get_or_create(name=tag_name)
      tags.append(tag)
    content.description = description
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
      try:
        parser.parse(content_dir, filename)
      except ContentParserException, e:
        logging.info('skipped {0} due to parsing error: {1}'.format(
          filename, e))

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
