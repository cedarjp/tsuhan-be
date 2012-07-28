# -*- coding:utf-8 -*-
from google.appengine.api import memcache
from google.appengine.api import urlfetch
import urllib
import json
import conf

class Moshimo:
    def __init__(self):
        self.authorization_code = 'aQqlGdbgQfVazJyB6SoNg8Sh2AqF0'
        self.content=None

    @staticmethod
    def get_category_name(category_code):
        if len(category_code)==2:
            return [conf.CATEGORY.get(category_code)]
        else:
            return list()

    @classmethod
    def get_sales_item(cls):
        instance=cls()
        result=instance.get_item_list(tags=u'ヒット実績あり'.encode('utf-8'),is_salable=1,
            exists_stock=1,list_per_page=48,page_index=0,sort_order='sales')

        try:
            data = result['ArticleSearch']['Articles']
        except KeyError:
            data = dict()
        return data

    @classmethod
    def get_new_item(cls):
        instance=cls()
        result=instance.get_item_list(is_newly=1,exists_stock=1,list_per_page=48,page_index=0,sort_order='newley')
        try:
            data=result['ArticleSearch']['Articles']
        except KeyError:
            data=dict()
        return data

    @classmethod
    def get_by_category(cls,category_code,list_per_page,page_index):
        data=dict()
        instance=cls()
        result=instance.get_item_list(article_category_code=category_code,require_tag_list=1,
            exists_stock=1,list_per_page=list_per_page,page_index=page_index,sort_order='sales')
        try:
            data['itemlist']=result['ArticleSearch']['Articles']
        except KeyError:
            data['itemlist']=dict()
        data['navi']=instance.get_parger('products',category_code,page_index+1,list_per_page)
        data['category_code']=category_code
        data['page']=page_index+1
        data['rows']=list_per_page
        try:
            data['prev']=data['navi'][page_index]
        except KeyError:
            data['prev']=None
        try:
            data['next']=data['navi'][page_index+2]
        except KeyError:
            data['next']=None
        return data

    @classmethod
    def get_by_tags(cls,tags,list_per_page,page_index):
        data=dict()
        instance=cls()
        result=instance.get_item_list(tags=tags.encode('utf-8'),require_tag_list=1,exists_stock=1,
            list_per_page=list_per_page,page_index=page_index,sort_order='sales')
        try:
            data['itemlist']=result['ArticleSearch']['Articles']
        except KeyError:
            data['itemlist']=dict()
        data['navi']=instance.get_parger('tags',tags,page_index+1,list_per_page)
        data['tags']=tags
        data['page']=page_index+1
        data['rows']=list_per_page
        try:
            data['prev']=data['navi'][page_index]
        except KeyError:
            data['prev']=None
        try:
            data['next']=data['navi'][page_index+2]
        except KeyError:
            data['next']=None
        return data

    @classmethod
    def get_by_search_word(cls,words,list_per_page,page_index):
        data=dict()
        instance=cls()
        words=words.strip()
        result=instance.get_item_list(
            words=words.encode('utf-8'),
            require_tag_list=1,
            exists_stock=1,
            list_per_page=list_per_page,
            page_index=page_index,
            sort_order='sales'
        )
        try:
            data['itemlist']=result['ArticleSearch']['Articles']
        except KeyError:
            data['itemlist']=dict()
        data['navi']=instance.get_parger('search',words,page_index+1,list_per_page)
        data['words']=words
        data['page']=page_index+1
        data['rows']=list_per_page
        try:
            data['prev']=data['navi'][page_index]
        except KeyError:
            data['prev']=None
        try:
            data['next']=data['navi'][page_index+2]
        except KeyError:
            data['next']=None
        return data

    @classmethod
    def get_by_article_id(cls,article_id):
        from core.models import Product
        data=dict()
        instance=cls()
        result=instance.get_item_list(article_id=article_id,require_tag_list=1)
        try:
            data['item']=result['ArticleSearch']['Articles'][0]
        except KeyError:
            data['item']={}
        data['product_content']=Product.get_by_key_name(article_id)
        return data

    def get_item_list(self, **kwds):
        mkey='item_list'
        params={'authorization_code':self.authorization_code}
        for k in kwds:
            v=kwds[k]
            if v is None:
                continue
            mkey+='_%s:%s'%(k,v)
            params[k]=v
        content=memcache.get(mkey)
        if content is None:
            payload=urllib.urlencode(params)
            url='http://api.moshimo.com/article/search.json?%s'%payload
            response=urlfetch.fetch(url,method=urlfetch.GET,follow_redirects=True)
            if response.status_code==200:
                content=json.loads(response.content)
                memcache.set(mkey,content,3600)
            else:
                content=None
        self.content=content
        return content

    def get_item_detail(self, article_id):
        mkey='item_detail%s'%article_id
        params={
            'authorization_code':self.authorization_code,
            'article_id':article_id,
            'require_tag_list':1,
            }
        content=memcache.get(mkey)
        if content is None:
            url='http://api.moshimo.com/article/search'
            payload=urllib.urlencode(params)
            response=urlfetch.fetch(url,payload=payload,method=urlfetch.POST,follow_redirects=True)
            if response.status==200:
                try:
                    content=response.content['ArticleSearch']['Articles'][0]
                    memcache.set(mkey,content,3600)
                except KeyError:
                    content={}
            else:
                content={}
        return content

    def get_category_list(self,category=None):
        mkey='category_list'
        if category is not None: mkey+='_%s'%category
        content=memcache.get(mkey)
        if content is None:
            params={'authorization_code':self.authorization_code}
            if category is not None:
                params['article_category_code']=category
            payload = urllib.urlencode(params)
            url = 'http://api.moshimo.com/category/list.json?%s'%payload
            response = urlfetch.fetch(url,payload=payload,method=urlfetch.GET,follow_redirects=True)
            if response.status_code==200:
                content=json.loads(response.content)
                memcache.set(mkey,content,3600)
        return content


    def get_parger(self,type,kwd,page,rows):
        navi = {}
        if self.content is None:
            return navi
        if int(self.content['ArticleSearch']['Rows']):
            num_pages=int(self.content['ArticleSearch']['Found'])/int(self.content['ArticleSearch']['Rows'])
        else:
            num_pages=1
        if page<=6:
            if num_pages>=10:
                for i in range(1,11):
                    navi[i]='/%s/%s/%s/%s'%(type,kwd,str(rows),str(i-1))
            else:
                for i in range(1,num_pages+1):
                    navi[i]='/%s/%s/%s/%s'%(type,kwd,str(rows),str(i-1))
        elif page+5>=num_pages:
            for i in range(num_pages-10,num_pages+1):
                navi[i]='/%s/%s/%s/%s'%(type,kwd,str(rows),str(i-1))
        else:
            if num_pages>=page+5:
                for i in range(page-5,page+5):
                    navi[i]='/%s/%s/%s/%s'%(type,kwd,str(rows),str(i-1))
            else:
                for i in range(page-5,num_pages+1):
                    navi[i]='/%s/%s/%s/%s'%(type,kwd,str(rows),str(i-1))
        return navi




