#!/usr/bin/env python
#-*- coding:utf-8 -*-

import webapp2
import webapp2_extras.jinja2

from google.appengine.ext import db

from .models import Entry, TextPost, PhotoPost, VideoPost, Tag

class BaseHandler(webapp2.RequestHandler):
    """
        Handler base to implement templates and other stuff.
    """
    @webapp2.cached_property
    def jinja2(self):
        """
           Returns a Jinja2 renderer cached in the app registry. 
        """
        return webapp2_extras.jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        """
            Renders a template and writes the result to the response.
        """
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)
        
class IndexHandler(BaseHandler):
    """
        Home page handler
    """
    model = Entry
    
    def get(self):
        tag = self.request.get('tag', None)
        
        qry = self.model.all()
        if tag:
            qry = qry.filter('tags =', unicode(tag))

        context = {
            'title': u'Hjkshdf Blog',
            'posts': qry,
            'tags': Tag.all(),
        }
        
        return self.render_response('blog.html', **context)

class EntryHandler(BaseHandler):
    """
        Entry info handler.
        Supports GET, POST, PUT and DELETE verbs to allow operation over
        entries.
    """
    model = Entry
    
    def get(self):
        """
            HTTP GET verb.
        """
        key = self.request.get('k', None)
        post = Entry.get(db.Key(key))
        
        self.response.content_type = post.mimetype
        return self.response.write(post.value)
        
        
class TextPostHandler(IndexHandler):
    model = TextPost

class PhotoPostHandler(IndexHandler):
    model = PhotoPost

class VideoPostHandler(IndexHandler):
    model = VideoPost
            
