# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
# Create your models here.
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

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

Status_Type = (
    ('0', 'wait'),
    ('1', 'rejected'),
)

from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=254, blank=True)
    last_name = models.CharField(max_length=254, blank=True)
    email = models.EmailField(blank=True, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/original.jpg', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    study_type = models.CharField(max_length=10, choices=Study_Type)
    faculty = models.CharField(max_length=250, blank=True)
    specialization = models.CharField(max_length=250, blank=True)
    year_of_study = models.CharField(max_length=10, choices=Year_Study)
    country = models.CharField(max_length=250, blank=True)
    county = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    nationality = models.CharField(max_length=250, blank=True)

    def get_address(self):
        address = '%s, %s' % (self.country, self.city)
        return address.strip()


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
    birth_date = models.DateField(null=True)
    study_type = models.CharField(max_length=10, choices=Study_Type)
    faculty = models.CharField(max_length=250)
    specialization = models.CharField(max_length=250)
    year_of_study = models.CharField(max_length=10, choices=Year_Study)
    motivation = models.TextField(max_length=500)
    status = models.CharField(max_length=10, choices=Status_Type, default='0')
    country = models.CharField(max_length=250, blank=True)
    county = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    nationality = models.CharField(max_length=250)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('web_page:applicant_details', kwargs={'pk': self.pk})

    def get_address(self):
        address = '%s, %s, %s' % (self.country, self.county, self.city)
        return address.strip()


class FaqCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('web_page:frequently_asked_questions', kwargs={'pk': self.pk})


class FrequentlyAskedQuestions(models.Model):
    faq_category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE)
    question = models.TextField(max_length=500, blank=True)
    answer = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.faq_category.name
