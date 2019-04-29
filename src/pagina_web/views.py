# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DetailView

from pagina_web.forms import ApplicationEnrollmentForm, FrequentlyAskedQuestionsForm
from pagina_web.models import ApplicationEnrollment, FaqCategory, FrequentlyAskedQuestions, User
from pagina_web.utils import send_email_application_enrollement, register_new_student, student_rejected


def redirect_home(request):
    return redirect("web_page:home_page")


class AboutView(TemplateView):
    template_name = "developers_details.html"


class UserProfileView(TemplateView):
    template_name = "user_profile.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['object'] = self.model.objects.get(pk=self.request.user.id)
        return context


class HomePageView(TemplateView):
    template_name = "home_page.html"


class ApplicationEnrollmentView(FormView):
    template_name = "application_enrollment.html"
    form_class = ApplicationEnrollmentForm

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


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('web_page:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


class ListFaqCategoryView(ListView):
    template_name = 'list_faq_category.html'

    def get_queryset(self):
        query = FaqCategory.objects.all().order_by("name")
        return query


class FrequentlyAskedQuestionsView(ListView):
    template_name = 'frequently_asked_questions.html'
    model = FrequentlyAskedQuestions

    def get_queryset(self):
        query = self.model.objects.filter(faq_category=self.kwargs.get('pk'))
        return query

    def get_context_data(self, **kwargs):
        context = super(FrequentlyAskedQuestionsView, self).get_context_data(**kwargs)
        context['category_pk'] = self.kwargs.get('pk')
        return context


def edit_faq(request, pk):
    faq = get_object_or_404(FrequentlyAskedQuestions, id=pk)

    if request.method == "POST":
        form = FrequentlyAskedQuestionsForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect('web_page:frequently_asked_questions', pk=faq.faq_category.pk)
    else:
        form = FrequentlyAskedQuestionsForm(instance=faq)
    template = "add_edit_faq.html"
    context = {
        'form': form,
        'instance': pk
    }
    return render(request, template, context)


def delete_faq(request, pk):
    faq = get_object_or_404(FrequentlyAskedQuestions, id=pk)
    if faq:
        faq.delete()
    return redirect('web_page:frequently_asked_questions', pk=faq.faq_category.pk)


class AddFAQView(FormView):
    template_name = "add_edit_faq.html"
    form_class = FrequentlyAskedQuestionsForm

    def form_valid(self, form):
        faq = form.save(commit=False)
        faq.faq_category_id = self.kwargs.get('pk')
        faq.save()
        messages.success(self.request, 'Successfully added.')
        return redirect('web_page:frequently_asked_questions', pk=self.kwargs.get('pk'))
