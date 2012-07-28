# -*- coding: utf-8 -*-
from __future__ import with_statement
"""
admin.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""


from kay.utils import (render_to_response,render_to_string)
from core.models import (Sitemap,FileData,TextFileData)
from google.appengine.ext import deferred
from google.appengine.ext import db
from google.appengine.api import memcache
from kay.auth.decorators import admin_required
from werkzeug import (
  unescape, redirect, Response,
)
# Create your views here.

@admin_required
def index(request):
    from core.forms import SearchForm
    form=SearchForm()
    return render_to_response('admin/index.html',{'form':form.as_widget()})

@admin_required
def sitemap(request):
    from admin.forms import SitemapForm
    from core.forms import SearchForm
    from core.models import Sitemap
    from google.appengine.ext import deferred
    sitemap_form=SitemapForm()
    search_form=SearchForm()
    if request.method=='POST' and sitemap_form.validate(request.form):
        if form['mode']==u'更新':
            deferred.defer(Sitemap.update_article_id,form['article_id'])
        else:
            deferred.defer(Sitemap.set_article_id,form['article_id'])
    return render_to_response('admin/sitemap.html', {'form':search_form.as_widget(),'sitemap_form': sitemap_form.as_widget()})


@admin_required
def product(request):
    from core.forms import ProductForm
    from core.forms import SearchForm
    product_form=ProductForm()
    search_form=SearchForm()
    if request.method=='POST' and product_form.validate(request.form):
        product_form.save(key_name=form['article_id'])
    return render_to_response('admin/product.html', {'form':search_form.as_widget(),'product_form': product_form.as_widget()})


def sitemap_create(request):
    deferred.defer(sitemap_create_batch)
    return Response('ok')
