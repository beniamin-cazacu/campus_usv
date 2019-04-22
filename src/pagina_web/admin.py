# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from pagina_web.models import Profile, ApplicationEnrollment


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'study_type', 'faculty', 'specialization', 'year_of_study')


admin.site.register(Profile, ProfileAdmin)


class ApplicationEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
    'first_name', 'last_name', 'email', 'study_type', 'faculty', 'specialization', 'year_of_study', 'status')


admin.site.register(ApplicationEnrollment, ApplicationEnrollmentAdmin)
