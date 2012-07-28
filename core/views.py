# -*- coding: utf-8 -*-
"""
core.views
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

import urllib
from kay.utils import render_to_response, url_for
from werkzeug import (
  unescape, redirect, Response,
)
from core.forms import SearchForm
from core.models import TextFileData
from moshimo import Moshimo

# Create your views here.


def index(request):
    u"""
    トップページ
    新入荷商品：Moshimo.get_new_item
    ヒット商品：Moshimo.get_sales_item
    """
    from moshimo import Moshimo
    from core.forms import SearchForm
    from kay.utils import render_to_response

    form=SearchForm(action='/search_post')
    salesitem_data=Moshimo.get_sales_item()
    newitem_data=Moshimo.get_new_item()

    return render_to_response('core/index.html', {
        'form':form.as_widget(),
        'newitem':newitem_data,
        'salesitem':salesitem_data,
    })

#カテゴリーページを表示
def products(request,category_code,list_per_page,page_index):
    form=SearchForm(action='/search_post')
    data=Moshimo.get_by_category(category_code,list_per_page,page_index)
    data['categories']=Moshimo.get_category_name(category_code)
    data['form']=form.as_widget()

    return render_to_response('core/product_list.html',data)

#カテゴリーページを表示
def tags(request,tags,list_per_page,page_index):
    form=SearchForm(action='/search_post')
    data=Moshimo.get_by_tags(tags,list_per_page,page_index)
    data['categories']=[u'タグ',tags]
    data['form']=form.as_widget()

    return render_to_response('core/product_list.html',data)

def search_post(request):
    form=SearchForm(action=url_for('core/search_post'))
    words=None
    if request.method=='POST' and form.validate(request.form):
        words=form['words'].strip()
        words=words.replace('/',' ')
    if words is None:
        return redirect(url_for('core/index'))
    else:
        return redirect(url_for('core/search',words=words,list_per_page=24,page_index=0))


#カテゴリーページを表示
def search(request,words,list_per_page,page_index):
    form=SearchForm(action=url_for('core/search_post'))
    data=Moshimo.get_by_search_word(words,list_per_page,page_index)
    data['categories']=[u'検索',words]
    data['form']=form.as_widget()

    return render_to_response('core/product_list.html', data)


#商品ページを表示
def detail(request,article_id):
    from core.models import Product
    form=SearchForm(action='/search_post')
    data=Moshimo.get_by_article_id(article_id)
    data['form']=form.as_widget()

    return render_to_response('core/detail.html', data)

def sitemap(request):
    from kay.utils import get_by_key_name_or_404
    f=get_by_key_name_or_404(TextFileData,'sitemap.xml')
    content=f.getData()
    return Response(content, content_type=f.filemimetype)

