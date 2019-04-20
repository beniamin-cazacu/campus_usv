# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.urls import reverse

Year_Study = (
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV'),
)
Study_Type = (
    ('master', 'master'),
    ('licence', 'licenta'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    study_type = models.CharField(max_length=10, choices=Study_Type)
    faculty = models.CharField(max_length=250, blank=True)
    specialization = models.CharField(max_length=250, blank=True)
    year_of_study = models.CharField(max_length=10, choices=Year_Study)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ApplicationEnrollment(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    birth_date = models.DateField(null=True, blank=True)
    study_type = models.CharField(max_length=10, choices=Study_Type)
    faculty = models.CharField(max_length=250, blank=True)
    specialization = models.CharField(max_length=250, blank=True)
    year_of_study = models.CharField(max_length=10, choices=Year_Study)
    motivation = models.TextField(max_length=500, blank=True)
    is_accepted = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('web_page:applicant_details', kwargs={'pk': self.id})
