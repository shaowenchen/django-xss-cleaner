# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings

from xss_cleaner.settings import sec_settings
from xss_cleaner.utils import clean_xss


logger = logging.getLogger(__name__)


class CleanXssMiddleware(object):

    def __init__(self):
        self.__escape_param_list = []
        self.__http_method_names = ['GET', 'POST']
        self.__level = sec_settings.XSS_LEVEL

    def process_view(self, request, view, args, kwargs):
        '''
        View处理前的
        '''
        if getattr(view, 'escape_clean', False):
            return None

        self.__escape_param_list = getattr(
            view, 'escape_clean_param') if hasattr(view,
                                                   'escape_clean_param') else []

        for method in self.__http_method_names:
            if hasattr(request, method):
                setattr(request,
                        method,
                        self.__escape_data(getattr(request, method)))
        return None

    def __escape_data(self, query_dict):
        '''
        参数转义
        '''
        data_copy = query_dict.copy()
        for _get_key, _get_value_list in data_copy.lists():
            new_value_list = []
            for _get_value in _get_value_list:
                if _get_key in self.__escape_param_list:
                    new_value = _get_value
                else:
                    new_value = clean_xss(text_string=_get_value,
                                          level=self.__level,
                                          extend=sec_settings.BLEACH_WHITE_LIST)

                if sec_settings.BLEACH_SHOW and new_value != _get_value:
                    if settings.DEBUG:
                        print('XSS : Transfer  %s  To  %s' % (
                            _get_value, new_value))
                    else:
                        logger.warning('XSS : Transfer  %s  To  %s' % (
                            _get_value, new_value))
                new_value_list.append(new_value)
            data_copy.setlist(_get_key, new_value_list)
        return data_copy
