# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase


class CleanXssTest(TestCase):
    is_assert = False
    is_print = True

    def test_get_a(self):
        data = {'title': '<aa src="http://src" class="getAClass">geta</aa> <a src=""> <script>'} # noqa
        right_text = {'title': '&lt;aa class="getAClass" src="http://src"&gt;geta&lt;/aa&gt; <a> &lt;script&gt;&lt;/script&gt;</a>'} # noqa
        response = self.client.get('/security/xss/bleach/test/', data)
        if self.is_print:
            print(data)
            print('geta result - %s' % json.loads(response.content).get('data', '')) # noqa
        if self.is_assert:
            self.assertEquals(right_text, json.loads(response.content).get('data', '')) # noqa

    def test_get_b(self):
        data = {'title': '<a href="http://href">getb</a><h1>H<h3>HHH'}
        right_text = {u'title': u'<a href="http://href">getb</a><h1>H</h1><h3>HHH</h3>'} # noqa
        response = self.client.get('/security/xss/bleach/test/', data)
        if self.is_print:
            print(data)
            print('getb result - %s' % json.loads(response.content).get('data', '')) # noqa
        if self.is_assert:
            self.assertEquals(right_text, json.loads(response.content).get('data', '')) # noqa

    def test_post_a(self):
        data = {'title': '<aa src="http://src" class="getAClass">geta</aa> <a src=""> <script>'} # noqa
        right_text = {u'title': u'&lt;aa class="getAClass" src="http://src"&gt;geta&lt;/aa&gt; <a> &lt;script&gt;&lt;/script&gt;</a>'} # noqa
        response = self.client.post('/security/xss/bleach/test/', data)
        if self.is_print:
            print(data)
            print('posta result - %s' % json.loads(response.content).get('data', '')) # noqa
        if self.is_assert:
            self.assertEquals(right_text, json.loads(response.content).get('data', '')) # noqa

    def test_post_b(self):
        data = {'title': '<a href="http://href">getb</a><h1>H<h3>HHH'}
        right_text = {u'title': u'<a href="http://href">getb</a><h1>H</h1><h3>HHH</h3>'} # noqa
        response = self.client.post('/security/xss/bleach/test/', data)
        if self.is_print:
            print(data)
            print('postb result - %s' % json.loads(response.content).get('data', '')) # noqa
        if self.is_assert:
            self.assertEquals(right_text, json.loads(response.content).get('data', '')) # noqa
