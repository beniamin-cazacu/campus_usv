# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, ListView, DetailView

from pagina_web.forms import ApplicationEnrollmentForm
from pagina_web.models import ApplicationEnrollment
from pagina_web.utils import send_email_application_enrollement, register_new_student, student_rejected


def redirect_home(request):
    return redirect("web_page:home_page")


class AboutView(TemplateView):
    template_name = "developers_details.html"


class HomePageView(TemplateView):
    template_name = "home_page.html"


class ApplicationEnrollmentView(FormView):
    template_name = "application_enrollment.html"
    form_class = ApplicationEnrollmentForm
    success_url = 'web_page:home_page'

    def form_valid(self, form):
        applicant = form.save(commit=False)
        form.save()
        applicant_id = applicant.pk
        first_name = form.cleaned_data.get('first_name')
        email = form.cleaned_data.get('email')
        current_site = get_current_site(self.request)
        domain = current_site.domain
        send_email_application_enrollement(applicant_id, first_name, first_name, email, domain)
        messages.success(self.request, 'Successfully enrolled.')
        return redirect('web_page:home_page')


class ListApplicantsView(ListView):
    template_name = 'list_applicants.html'

    def get_queryset(self):
        query = ApplicationEnrollment.objects.all().order_by("status")
        return query


class ApplicantDetailsView(DetailView):
    template_name = 'applicant_details.html'
    model = ApplicationEnrollment

    def get_context_data(self, **kwargs):
        context = super(ApplicantDetailsView, self).get_context_data(**kwargs)
        context['object'] = self.model.objects.get(pk=self.kwargs.get('pk'))
        return context


def response_application(request, pk, response_id):
    """ Response for student application (accepted or rejected) and send email
        @:param pk - student id
        @:param response_id (0 - rejected , 1 - accepted)
        """
    student = ApplicationEnrollment.objects.get(id=pk)
    current_site = get_current_site(request)
    domain = current_site.domain
    if response_id == '1':
        register_new_student(student, domain)
        student.delete()
    else:
        student_rejected(student, domain)
        student.status = '1'
        student.save()
    return redirect('web_page:list_applicants')
