from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Job(models.Model):
    '''
    title: job title
    description: job description
    city: city where job is located
    state: state where job is located
    application: link to application process
    created_at: date/time job was created
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    application = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Job")
        verbose_name_plural =("Jobs")


