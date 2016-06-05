#! /usr/bin/env python
# -*- coding:utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "app/root/index.html"

    def get(self, request):
        ctxt = {}
        return render_to_response(self.template_name,
                                  RequestContext(request, ctxt))

    def post(self, request):
        ctxt = {
            'is_succusessed': True
        }
        return render_to_response(self.template_name,
                                  RequestContext(request, ctxt))
