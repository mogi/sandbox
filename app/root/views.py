#! /usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from ast import literal_eval

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView, RedirectView

from app.apis import twitter as tw


class IndexView(TemplateView):
    template_name = "app/root/index.html"

    def get_context_data(self, **kwargs):
        ctxt = super(IndexView, self).get_context_data(**kwargs)
        key = kwargs.get("auth_key")
        if key:
            res, content = tw.get_cache_tw_result(key)
            ctxt["res"] = res if res else None
            ctxt["content"] = content if content else None
            ctxt["tweet_succeed"] = True
            tw.delete_cache(key)
        else:
            ctxt["tweet_succeed"] = False
        return ctxt

class CallbackView(RedirectView):
    pattern_name = "index"
    permanent = False


    def get(self, request, *args, **kwargs):
        msg = cache.get('app.root.view.post::msg')
        key = request.GET["oauth_token"]
        secret = tw.get_cache_auth_secret(key)
        verifier = request.GET["oauth_verifier"]

        responce, content = tw.tweet_with_auth(msg, key, secret, verifier)
        return HttpResponseRedirect(reverse("index", kwargs={"auth_key": key}))


class PostTwitterView(RedirectView):
    pattern_name = "index"
    permanent = False

    def post(self, request, *args, **kwargs):
        cache.set('app.root.view.post::msg', request.POST['message'], 300)
        callback_url = request.build_absolute_uri(reverse("callback"))
        authorize_url = tw.auth(callback_url)
        return HttpResponseRedirect(authorize_url)
