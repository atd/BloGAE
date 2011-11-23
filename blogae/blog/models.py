#!/usr/bin/env python
#-*- coding:utf-8 -*-

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

import webapp2_extras.json

ENTRY_TYPE_TEXT = 0
ENTRY_TYPE_PHOTO = 1
ENTRY_TYPE_VIDEO = 2
ENTRY_TYPES = (
    (ENTRY_TYPE_TEXT, 'Text post'),
    (ENTRY_TYPE_PHOTO, 'Photo post'),
    (ENTRY_TYPE_VIDEO, 'Video post'),
)

class Entry(polymodel.PolyModel):
    _TYPE = None
    _MIMETYPE = None
    """
        Post base class.
    """
    title = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    author = db.UserProperty(auto_current_user_add=True)
    draft = db.BooleanProperty(default=True)
    tags = db.StringListProperty()
    hits = db.IntegerProperty(default=0)
    rate = db.FloatProperty(default=float(0))
    
    @property
    def type(self):
        return self._TYPE
        
    @property
    def mimetype(self):
        return self._MIMETYPE
        
    @property
    def value(self):
        raise NotImplementedError
        
    def toHTML(self):
        """
            Returns entry HTML presentation.
        """
        raise NotImplementedError
        
    @property
    def url(self):
        """
            Returns a uri to entry.
        """
        return u'/entry/?k=%s' % self.key()
        
    def asDict(self):
        """
            Returns a dict representacion of entry.
        """
        return {
            'key': self.key.urlsafe(),
            'created': self.created.strftime("%d/%m/%Y %H:%M"),
            'updated': self.updated.strftime("%d/%m/%Y %H:%M"),
            'author': self.author.nickname(),
            'draft': self.draft,
            'tags': self.tags,
            'url': self.url,
        }
        
    def toJSON(self):
        """
            Returns a JSON representation of entry.
        """
        return webapp2_extras.json.encode(self.asDict())
        
    def add_rate(self, rate):
        """
            Adds one rate to total rating.
        """
        self.rate = self.rate + (rate - self.rate)/(self.hits + 1)
        self.hits += 1
        self.put()
        return self.rate
        
class Tag(db.Model):
    """
        Tags registry.
    """
    tag = db.StringProperty(required=True)
        
class Comment(db.Model):
    """
        Post comment.
    """
    entry = db.ReferenceProperty(Entry, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    author = db.UserProperty(auto_current_user_add=True)
    body = db.TextProperty(required=True)    

class TextPost(Entry):
    """
        Text post.
    """
    _TYPE = ENTRY_TYPE_TEXT
    _MIMETYPE = 'text/html'
    post = db.TextProperty()
    
    def toHTML(self):
        return self.post
        
    @property
    def value(self):
        return self.post
    
class PhotoPost(Entry):
    """
        Photo post.
    """
    _TYPE = ENTRY_TYPE_PHOTO
    _MIMETYPE = 'image/png'
    photo = db.BlobProperty()
    
    def toHTML(self):
        tag = u'<img src="%s" alter="%s" title="%s" />'
        return tag % (self.url, self.title, self.title)
    
    @property
    def value(self):
        return self.photo

class VideoPost(Entry):
    """
        Video post.
    """
    _TYPE = ENTRY_TYPE_VIDEO
    _MIMETYPE = 'text/html'
    video = db.LinkProperty()
    
    def toHTML(self):
        tag = u'<iframe width="560" height="315" src="%s" frameborder="0" allowfullscreen></iframe>'
        return tag % self.video
        
    @property
    def value(self):
        return ''

