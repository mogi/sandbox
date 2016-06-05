#! /usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, RedirectView


class IndexView(TemplateView):
    template_name = "app/root/index.html"

    def get_context_data(self, **kwargs):
        ctxt = super(IndexView, self).get_context_data(**kwargs)
        return ctxt


class PostTwitterView(RedirectView):
    pattern_name = "index"

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['message'])
        article.update_counter()
        return super(PostTwitterView, self).get_redirect_url(*args, **kwargs)


class AuthTwitterView(RedirectView):
    pattern_name = "index"

    def get_redirect_url(self, *args, **kwargs):
        return super(PostTwitterView, self).get_redirect_url(*args, **kwargs)
