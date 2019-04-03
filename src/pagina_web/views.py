# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# @login_required(login_url='{% url "login" %}')
class AboutView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "pagina_prezentare.html"


class PrincipalPage(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "principal_page.html"
