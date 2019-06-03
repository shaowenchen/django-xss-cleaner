# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from xss_cleaner.decorators import escape_clean


class TestView(View):
    res = {
        'result': True,
        'data': [],
        'message': '',
        'code': 0
    }

    @method_decorator(escape_clean)
    def dispatch(self, *args, **kwargs):
        return super(TestView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.res['data'] = request.GET
        self.res['message'] = 'GET Method'
        return HttpResponse(
            json.dumps(self.res),
            content_type='application/json')

    def post(self, request, *args, **kwargs):
        self.res['data'] = request.POST
        self.res['message'] = 'POST Method'
        return HttpResponse(
            json.dumps(self.res),
            content_type='application/json')
