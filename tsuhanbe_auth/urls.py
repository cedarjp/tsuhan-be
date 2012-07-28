# -*- coding: utf-8 -*-
# tsuhanbe_auth.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('tsuhanbe_auth/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'tsuhanbe_auth/index': 'tsuhanbe_auth.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='tsuhanbe_auth.views.index'),
  )
]

