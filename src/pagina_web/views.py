# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

# @login_required(login_url='{% url "login" %}')
from pagina_web.forms import ApplicationEnrollmentForm


def redirect_home(request):
    return redirect("web_page:home_page")


class AboutView(TemplateView):
    template_name = "developers_details.html"


#
# class PrincipalPage(LoginRequiredMixin, TemplateView):
#     login_url = 'login'
#     template_name = "home_page.html"

class HomePageView(TemplateView):
    template_name = "home_page.html"


class ApplicationEnrollmentView(FormView):
    template_name = "application_enrollment.html"
    form_class = ApplicationEnrollmentForm
    success_url = 'web_page:home_page'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully enrolled.')
        return HttpResponseRedirect(self.request.path)
        # return redirect('web_page:home_page')
