# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

# @login_required(login_url='{% url "login" %}')
from pagina_web.forms import ApplicationEnrollmentForm


class AboutView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "developers_details.html"


#
# class PrincipalPage(LoginRequiredMixin, TemplateView):
#     login_url = 'login'
#     template_name = "principal_page.html"

class PrincipalPageView(TemplateView):
    template_name = "principal_page.html"


class ApplicationEnrollmentView(FormView):
    template_name = "application_enrollment.html"
    form_class = ApplicationEnrollmentForm
    success_url = 'principal_page'

    def form_valid(self, form):
        form.save()
        return redirect('principal_page')
