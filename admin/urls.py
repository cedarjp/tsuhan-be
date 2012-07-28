# -*- coding: utf-8 -*-
# admin.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('admin/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'admin/index': 'admin.views.index',
}
"""

from kay.routing import (
    ViewGroup, Rule
    )

view_groups = [
    ViewGroup(
        Rule('/', endpoint='index', view='admin.views.index'),
        Rule('/sitemap_create', endpoint='sitemap_create', view='admin.views.sitemap_create'),
        Rule('/product', endpoint='product', view='admin.views.product'),
        Rule('/sitemap', endpoint='sitemap', view='admin.views.sitemap'),
    )
]

