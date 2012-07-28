# -*- coding: utf-8 -*-
"""
tsuhanbe_auth.views
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
from kay.utils import render_to_response
from kay.auth.decorators import (admin_required, login_required)
from kay.utils.paginator import Paginator, InvalidPage, EmptyPage
from tsuhanbe_auth.models import User

# Create your views here.

#@admin_required
@admin_required
def index(request):
    user=User.all()
    paginator=Paginator(user,25)
    try:
        page = int(request.args.get('page', '1'))
    except ValueError:
        page = 1
    try:
        contacts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('tsuhanbe_auth/index.html', {"contacts": contacts})

