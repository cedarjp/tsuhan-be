# -*- coding: utf-8 -*-
# core.models

from google.appengine.ext import db

# Create your models here.

#key_name:Moshimo article_id
class Product(db.Model):
    article_id=db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    updated=db.DateTimeProperty(auto_now=True)
    created=db.DateTimeProperty(auto_now_add=True)


class Sitemap(db.Model):
    article_id=db.StringListProperty(indexed=False)
    count=db.IntegerProperty(indexed=False)

    @classmethod
    def update_article_id(cls,article_id,query=None,cursor=None):
        from google.appengine.ext import deferred
        if query is None:
            query=cls.all()
        if cursor is not None:
            query.with_cursor(cursor)
        if query.count(limit=1):
            db.delete_async([q for q in query.run(limit=50)])
            cursor=query.cursor()
            deferred.defer(cls.update_article_id,article_id,query,cursor)
        else:
            deferred.defer(cls.set_article_id,article_id)



    @classmethod
    def set_article_id(cls,article_id):
        from google.appengine.ext import deferred
        if article_id[:5000]:
            instance=cls(
                article_id=article_id[:5000],
                count=len(article_id[:5000]),
            )
            db.put_async(instance)
            del article_id[:5000]
            if article_id:
                deferred.defer(cls.set_article_id,article_id)

    @classmethod
    def create_sitemap(cls,query=None,cursor=None,article_ids=None):
        from google.appengine.ext import deferred
        from kay.utils import render_to_string
        if query is None:
            query=cls.all()
        if cursor is not None:
            query.with_cursor(cursor)
        if article_ids is None:
            article_ids=list()
        if query.count(limit=1):
            for q in query.run(limit=50):
                article_ids.extend(q.article_id)
            cursor=query.cursor()
            deferred.defer(cls.create_sitemap,query,cursor,article_ids)
        else:
            sitemaps=list()
            for id in article_id:
                sitemaps.append({'loc':'http://www.2han.be/detail/%s'%id,})
            content = render_to_string('core/sitemap.xml', {
                'sitemaps':sitemaps
            })
            deferred.defer(TextFileData.set_sitemap,content)


    
class FileData(db.Model):
    filename = db.StringProperty(multiline=False)
    filemimetype = db.StringProperty(multiline=False)
    date     = db.DateTimeProperty(auto_now_add=True)

    def getData(self):
        data = []
        query=FileDataChunk.all().filter('master = ',self.key()).order('seq')
        for chunk in query:
            data.append(chunk.chunk)
        return ''.join(data)
    
    def insertData(self,data):
        for i in range( len(data) / 500000 + 1):
            chunk = FileDataChunk()
            chunk.master = self.key()
            chunk.seq = i
            chunk.chunk = db.Blob(data[i*500000:(i+1)*500000 ])
            chunk.put()
            
    def delete(self):
        query=FileDataChunk.all().filter('master = ',self.key())
        for chunk in query:
            chunk.delete()
        super(FileData,self).delete()

class FileDataChunk(db.Model):
    master= db.ReferenceProperty(FileData)
    seq   = db.IntegerProperty()
    chunk = db.BlobProperty()

    
class TextFileData(db.Model):
    filename = db.StringProperty(multiline=False)
    filemimetype = db.StringProperty(multiline=False)
    date     = db.DateTimeProperty(auto_now_add=True)


    @classmethod
    def set_sitemap(cls,content):
        instance=cls.get_by_key_name('sitemap.xml')
        if instance is not None:
            instance.delete()
        instance=TextFileData(
            key_name='sitemap.xml',
            filename='sitemap.xml',
            filemimetype='application/xml',
        )
        instance.insertData(data=content)
        instance.put()


    def getData(self):
        data = []
        query=TextFileDataChunk.all().filter('master = ',self.key()).order('seq')
        for chunk in query:
            data.append(chunk.chunk)
        return ''.join(data)
    
    def insertData(self,data):
        for i in range( len(data) / 500000 + 1):
            chunk = TextFileDataChunk()
            chunk.master = self.key()
            chunk.seq = i
            chunk.chunk = data[i*500000:(i+1)*500000 ]
            chunk.put()
            
    def delete(self):
        query=TextFileDataChunk.all().filter('master = ',self.key())
        for chunk in query:
            chunk.delete()
        super(TextFileData,self).delete()

class TextFileDataChunk(db.Model):
    master= db.ReferenceProperty(TextFileData)
    seq   = db.IntegerProperty()
    chunk = db.TextProperty()


