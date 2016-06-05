#! /usr/bin/env python
# -*- coding:utf-8 -*-
from .root import get_urlpatterns as root_urlpatterns

urlpatterns = []
urlpatterns += root_urlpatterns()
