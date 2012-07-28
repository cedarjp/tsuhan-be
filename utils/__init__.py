# -*- coding:utf-8 -*-

import re

def int_add_comma(value):
    value = to_long(value)
    if value is not None:
        regex = re.compile(r'(\d)(?=(?:\d{3})+$)')
        return regex.sub(r'\1,', str(value))
    else:
        return None

def to_long(value):
  return long(value) if re.match(r'^(?![-+]0+$)[-+]?([1-9][0-9]*)?[0-9](\.[0-9]+)?$', '%s' %value) else None

def to_int(value):
  return int(value) if re.match(r'^(?![-+]0+$)[-+]?([1-9][0-9]*)?[0-9](\.[0-9]+)?$', '%s' %value) else None

def to_str(value):
  return str(value)

def get_by_key(value):
  return db.get(value)

def is_none_empty(value):
  if value is None:
    return False
  elif isinstance(value,list) and value == []:
    return False
  elif isinstance(value,dict) and value == {}:
    return False
  elif value == '':
    return False
  else:
    return True