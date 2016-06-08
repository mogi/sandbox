#! /usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from ast import literal_eval

from django import http
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView, RedirectView

from app.models.oauth.twitter import auth, tweet, tweet_with_auth


class IndexView(TemplateView):
    template_name = "app/root/index.html"

    def get_context_data(self, **kwargs):
        ctxt = super(IndexView, self).get_context_data(**kwargs)

        key = cache.get('app.root.view.post::access_token_key')
        secret = cache.get('app.root.view.post::access_token_secret')
        ctxt["authed"] = True if key and secret else False

        res = cache.get('app.root.view.post::tweet_responce')
        ctxt["res"] = res if res else None
        content = cache.get('app.root.view.post::tweet_content')
        ctxt["content"] = content if content else None
        if res and content:
            ctxt["tweet_succeed"] = content.find("errors") < 0
            cache.delete_many(['app.root.view.post::tweet_responce',
                               'app.root.view.post::tweet_content'])
        return ctxt

class CallbackView(RedirectView):
    pattern_name = "index"
    permanent = False


    def get(self, request, *args, **kwargs):
        msg = cache.get('app.root.view.post::msg')
        key = request.GET["oauth_token"]
        secret = cache.get('app.root.view.post::oauth_token_secret')
        verifier = request.GET["oauth_verifier"]

        responce, content = tweet_with_auth(msg, key, secret, verifier)
        return super(CallbackView, self).get(request, *args, **kwargs)


class PostTwitterView(RedirectView):
    pattern_name = "index"
    permanent = False

    def post(self, request, *args, **kwargs):
        key = cache.get('app.root.view.post::access_token_key')
        secret = cache.get('app.root.view.post::access_token_secret')
        if key and secret:
            msg = request.POST['message']
            responce, content =  tweet(msg, key, secret)
            return http.HttpResponseRedirect(reverse("index"))
        else:
            callback_url = request.build_absolute_uri(reverse("callback"))
            authorize_url = auth(callback_url)

            cache.set('app.root.view.post::msg', request.POST['message'], 300)
            return http.HttpResponseRedirect(authorize_url)
