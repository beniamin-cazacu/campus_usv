# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from pagina_web.models import Profile, ApplicationEnrollment, User, FaqCategory, FrequentlyAskedQuestions


class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')


admin.site.register(User, UsersAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'birth_date', 'study_type', 'faculty', 'specialization', 'year_of_study')


admin.site.register(Profile, ProfileAdmin)


class ApplicationEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'study_type', 'faculty', 'specialization', 'year_of_study', 'status')


admin.site.register(ApplicationEnrollment, ApplicationEnrollmentAdmin)

admin.site.register(FaqCategory)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('faq_category', 'question')


admin.site.register(FrequentlyAskedQuestions, FAQAdmin)
