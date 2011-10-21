"""
clean_cv_db.py

Usage:
  clean_cv_db.py

Cleans out all CV data in the database.
"""

import logging
from cv.models import Content, Tag

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
  for model in [Content, Tag]:
    logging.info('cleaning out data for model {0}'.format(model.__name__))
    model.objects.all().delete()
