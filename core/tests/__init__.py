# -*- coding:utf-8 -*-

from werkzeug import BaseResponse,  Request
from kay.app import get_application
from kay.utils import url_for
from kay.utils.test import (
    init_recording, get_last_context, get_last_template, disable_recording,Client
    )

from kay.ext.testutils.gae_test_base import GAETestBase

class TsuhanTest(GAETestBase):
    CLEANUP_USED_KIND = False
    USE_PRODUCTION_STUBS = True
    KIND_NAME_UNSWAPPED=False
    USE_REMOTE_STUBS=False

    def setUp(self):
        init_recording()
        app = get_application()
        self.client = Client(app, BaseResponse)
        self.client.test_login()

    def tearDown(self):
        self.client.test_logout()
        disable_recording()

    def test_index(self):
        response = self.client.open(
            path=url_for('core/index'),
            method='GET',
            data=dict(),
        )
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        response = self.client.open(
            path=url_for('core/products',category_code='01',list_per_page=20,page_index=0),
            method='GET',
            data=dict(),
        )
        self.assertEqual(response.status_code, 200)

    def test_tags(self):
        response = self.client.open(
            path=url_for('core/tags',tags=u'タグ',list_per_page=20,page_index=0),
            method='GET',
            data=dict(),
        )
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.open(
            path=url_for('core/search',words=u'検索ワード',list_per_page=20,page_index=0),
            method='GET',
            data=dict(),
        )
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.open(
            path=url_for('core/detail',article_id='421135'),
            method='GET',
            data=dict(),
        )
        self.assertEqual(response.status_code, 200)

    def test_sitemap(self):
        response = self.client.open(
            path=url_for('core/sitemap'),
            method='GET',
            data=dict(),
        )
        self.assertEqual(response.status_code, 404)

