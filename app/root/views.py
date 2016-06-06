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


from django.core.urlresolvers import reverse
class PostTwitterView(RedirectView):
    pattern_name = "index"
    permanent=False

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['message'])
        article.update_counter()
        return super(PostTwitterView, self).get_redirect_url(*args, **kwargs)

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


class AuthTwitterView(RedirectView):
    pattern_name = "index"
    permanent=False

    def get_redirect_url(self, *args, **kwargs):
        return super(PostTwitterView, self).get_redirect_url(*args, **kwargs)
