# -*- coding: utf-8 -*-
import bleach

from xss_cleaner.settings import sec_settings


def clean_xss(text_string, level='high', extend={}):
    '''
    使用 Bleach 消毒字符串，kwargs 中如果没有配置参数，则去 level 套餐中取。
    kwargs 的格式可以参考 settings 中 BLEACH_HIGH。
    '''
    bleach_allow = getattr(sec_settings, '_'.join(['BLEACH', level.upper()]))
    attributes = {}
    for k in set(
            bleach_allow['attributes'].keys()
            ).union(set(extend.get('attributes', {}).keys())):
        attributes[k] = list(set(
                bleach_allow['attributes'].get(k, [])
                ).union(set(extend.get('attributes', {}).get(k, []))))
    return bleach.clean(text=text_string,
                        tags=list(set(bleach_allow['tags']).union(
                                set(extend.get('tags', [])))),
                        attributes=attributes,
                        styles=list(set(bleach_allow['styles']).union(
                                set(extend.get('styles', [])))),
                        strip=extend.get('strip', bleach_allow['strip']),
                        strip_comments=extend.get(
                                'strip_comments',
                                bleach_allow['strip_comments']))
