# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "pagina_prezentare.html"
