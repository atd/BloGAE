#-*- coding: utf-8 -*-
'''Urls for blog app'''
from webapp2 import Route
from webapp2_extras import routes

urls = [
    routes.HandlerPrefixRoute('blog.handlers.', [
        Route(r'/', handler='IndexHandler', name='home'),
        Route(r'/textpost/', handler='TextPostHandler', name='textpost'),
        Route(r'/photopost/', handler='PhotoPostHandler', name='photopost'),
        Route(r'/videopost/', handler='VideoPostHandler', name='videopost'),
        Route(r'/entry/', handler='EntryHandler', name='entry'),
    ]),
    routes.PathPrefixRoute('/admin', [
        routes.HandlerPrefixRoute('admin.handlers.', [
            Route(r'/', handler='AdminHandler', name='admin'),
            Route(r'/textpost/', handler='TextPostHandler', name='admin-textpost'),
            Route(r'/photopost/', handler='PhotoPostHandler', name='admin-photopost'),
            Route(r'/videopost/', handler='VideoPostHandler', name='admin-videopost'),
        ])
    ]),
]
