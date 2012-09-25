import datetime

def datetime_to_date(dt):
  return datetime.date(dt.year, dt.month, dt.day)

def date_now():
  return datetime_to_date(datetime.datetime.now())
