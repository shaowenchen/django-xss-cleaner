# -*- coding: utf-8 -*-
from django.conf import settings


DEFAULT = {
    'BLEACH_HIGH': {
        'tags': ['a', 'img', 'strong', 'p', 'div', 'span', 'h1',
                 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'ul', 'ol',
                 'tr', 'th', 'td', 'li'],
        'attributes': {'a': ['href', 'title', 'target'],
                       'img': ['width', 'height', 'src']},
        'styles': [],
        'strip': False,
        'strip_comments': False
    },
    'BLEACH_LOW': {
        'tags': ['a', 'img', 'br', 'strong', 'b', 'code', 'pre', 'p',
                 'div', 'em', 'span', 'h1', 'h2', 'h3', 'h4', 'h5',
                 'h6', 'table', 'ul', 'ol', 'tr', 'th', 'td', 'hr', 'li', 'u'],
        'attributes': {'a': ['href', 'title', 'target'],
                       'img': ['width', 'height', 'src', 'alt'],
                       '*': ['class', 'style']},
        'styles': [],
        'strip': False,
        'strip_comments': False
    },
    'BLEACH_WHITE_LIST': {
        'tags': [],
        'attributes': {},
        'styles': [],
        'strip': False,
        'strip_comments': False
    },
    'XSS_LEVEL': 'HIGH',
    'BLEACH_SHOW': True
}


class SecuritySettings(object):
    def __getattr__(self, attr):
        if attr not in DEFAULT.keys():
            raise AttributeError("Invalid security setting: '%s'" % attr)
        return getattr(settings, attr, DEFAULT.get(attr))


sec_settings = SecuritySettings()
