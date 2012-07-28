# -*- coding: utf-8 -*-
# core.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('core/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'core/index': 'core.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='core.views.index'),
    Rule('/search_post', endpoint='search_post', view='core.views.search_post'),
    Rule('/sitemap', endpoint='sitemap', view='core.views.sitemap'),
    Rule('/products/<string:category_code>/<int:list_per_page>/<int:page_index>', endpoint='products', view='core.views.products'),
    Rule('/tags/<string:tags>/<int:list_per_page>/<int:page_index>', endpoint='tags', view='core.views.tags'),
    Rule('/search/<string:words>/<int:list_per_page>/<int:page_index>', endpoint='search', view='core.views.search'),
    Rule('/detail/<string:article_id>', endpoint='detail', view='core.views.detail'),
  )
]

