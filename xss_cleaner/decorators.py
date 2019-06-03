# -*- coding: utf-8 -*-

from django.utils.decorators import available_attrs
from django.utils.functional import wraps


def escape_clean(view_func):
    """
    Clean XSS豁免，被此装饰器修饰的action可以不进行中间件escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_clean = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_clean_param(*param_list, **param_list_dict):
    """
    此装饰器用来豁免某个view函数的某个参数
    @param param_list: 参数列表[ ]
    @return:
    """
    def _escape_exempt_param(view_func):
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)
        if param_list_dict.get('param_list'):
            wrapped_view.escape_clean_param = param_list_dict['param_list']
        else:
            wrapped_view.escape_clean_param = list(param_list)
        return wraps(view_func,
                     assigned=available_attrs(view_func))(wrapped_view)
    return _escape_exempt_param
