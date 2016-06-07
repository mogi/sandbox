#! /usr/bin/env python
# -*- coding:utf-8 -*-
from django import http
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView, RedirectView
from app.models.oauth.twitter import auth


class IndexView(TemplateView):
    template_name = "app/root/index.html"

    def get_context_data(self, **kwargs):
        ctxt = super(IndexView, self).get_context_data(**kwargs)
        return ctxt


class AuthTwitterView(RedirectView):
    permanent = False

    def post(self, request, *args, **kwargs):
        callback_url = request.build_absolute_uri(reverse("callback"))
        authorize_url = auth(callback_url)
        return http.HttpResponseRedirect(authorize_url)

class CallbackView(RedirectView):
    pattern_name = "index"
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return super(CallbackView, self).get_redirect_url(*args, **kwargs)


class PostTwitterView(RedirectView):
    pattern_name = "index"
    permanent = False

    def post(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        if url:
            if self.permanent:
                return http.HttpResponsePermanentRedirect(url)
            else:
                return http.HttpResponseRedirect(url)
        else:
            logger.warning(
                'Gone: %s', request.path,
                extra={'status_code': 410, 'request': request}
            )
            return http.HttpResponseGone()

    def get_redirect_url(self, *args, **kwargs):
        return super(PostTwitterView, self).get_redirect_url(*args, **kwargs)
