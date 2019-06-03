# -*- coding: utf-8 -*-
from django.conf.urls import patterns

from xss_cleaner.views import TestView

urlpatterns = patterns(
    '',
    (r'^xss/bleach/test/$', TestView.as_view())
)
