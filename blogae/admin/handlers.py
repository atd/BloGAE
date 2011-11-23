#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2

import webapp2
import webapp2_extras.json

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import urlfetch

from blog.handlers import BaseHandler
import blog.models
from blog.models import Entry, TextPost, PhotoPost, VideoPost, Tag
from google.appengine.api import users

def get_key_from_body(body):
    """
        Get key argum,ent from request body.
        Used in DELETE method to get key info.
    """
    start = body.find('k=') + len('k=')
    end = len(body)
    return body[start:end]
    
def resize(img, dimensions_limits=((0, 0), (500, 500))):
    """
        Resizes a image with limit dimensions given.
    """
    
    image = images.Image(img)
    ratio = 1
    height_min = float(dimensions_limits[0][0])
    width_min = float(dimensions_limits[0][1])
    height_max = float(dimensions_limits[1][0])
    width_max = float(dimensions_limits[1][1])
    if image.width <= width_max:
        if image.height > height_max:
            ratio = height_max / image.height
    else:
        ratio = width_max / image.width
        new_image_height = image.height * ratio
        if new_image_height > height_max:
            ratio = height_max / image.height
    width = int(image.width * ratio)
    height = int(image.height * ratio)
    image.resize(width=width, height=height)
    
    return image.execute_transforms()
    
def get_tags(tags):
    """
        Get tags from request info.
    """
    assert isinstance(tags, basestring)
    
    # comma separator
    tags = tags.split(',')
    for tag in tags:
        tag = tag.strip()
        Tag.get_or_insert(tag, tag=tag)
        
    return tags

class AdminHandler(BaseHandler):
    """
        Base admin page handler.
    """
    model = Entry
    template = 'admin.html'
    type = ''
    
    def get(self):
        user = users.get_current_user()
        
        context = {
            'title': 'Blog Admin',
            'user': user,
            'logout_url': users.create_logout_url(self.uri_for('home')),
            'entries': self.model.all(),
            'type': self.type,
        }
        self.render_response(self.template, **context)
        
    def delete(self):
        key = get_key_from_body(self.request.body)
        
        if key:
            instance = Entry.get(db.Key(key))
            instance.delete()
        
class TextPostHandler(AdminHandler):
    """
        Text post admin handler.
    """
    model = TextPost
    template = 'textpost.html'
    type = 'Text'
    
    def post(self):
        # get arguments
        args = {}
        title = self.request.get('title', None)
        post = self.request.get('post', None)
        tags = self.request.get('tags', None)
        
        if title: args['title'] = title
        if post: args['post'] = post
        if tags: args['tags'] = get_tags(tags)
        
        new_model = self.model(**args)
        new_model.put()
        return self.redirect_to('admin-textpost')
    
class PhotoPostHandler(AdminHandler):
    """
        Photo post admin handler.
    """
    model = PhotoPost
    template = 'photopost.html'
    type = 'Photo'
    
    def post(self):
        # get arguments
        args = {}
        title = self.request.get('title', None)
        photo = self.request.get('photo', None)
        photo_url = self.request.get('url', None)
        tags = self.request.get('tags', None)
        
        if title: args['title'] = title
        if photo_url:
            req = urlfetch.fetch(photo_url)
            if req.status_code == 200:
                photo = req.content
            else:
                if not photo:
                    return self.abort(404, u'Imagen no encontrada')
                    
        if photo: args['photo'] = resize(photo)
        if tags: args['tags'] = get_tags(tags)
        
        new_model = self.model(**args)
        new_model.put()
        return self.redirect_to('admin-photopost')
    
class VideoPostHandler(AdminHandler):
    """
        Video post admin handler.
    """
    model = VideoPost
    template = 'videopost.html'
    type = 'Video'
    
    def post(self):
        # get arguments
        args = {}
        title = self.request.get('title', None)
        video = self.request.get('video', None)
        tags = self.request.get('tags', None)
        
        if title: args['title'] = title
        if video:
            req = urlfetch.fetch(video)
            if req.status_code == 200:
                args['video'] = video
            else:
                self.abort(404, u'Vídeo no encontrado')
        if tags: args['tags'] = get_tags(tags)
        
        new_model = self.model(**args)
        new_model.put()
        return self.redirect_to('admin-videopost')


