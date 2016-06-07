# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url, include
from .views import IndexView, AuthTwitterView, PostTwitterView, CallbackView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^twitter/auth$', AuthTwitterView.as_view(), name="auth"),
    url(r'^twitter/callback$', CallbackView.as_view(), name="callback"),
    url(r'^twitter/post$', PostTwitterView.as_view(), name="post-twitter"),
)
