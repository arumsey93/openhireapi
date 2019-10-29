from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    '''
    description: This class creates a customer and its properties
    author: Group Code
    properties:
      first_name: user first name
      last_name: user last name
      email: user email address
      date_joined: the date of user account creation
      isActive: boolean to list if the user account is active or not
      linkedin: link to users linkedin
      github: link to users github
      resume: link to users resume
      portofolio: link to users portfolio website
      created_at: date/time created
      profile_image: users profile image
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    linkedin = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    resume = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)
    codingchallenge = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='openhire\openhireapi\profile_image')

    def __str__(self):
        return f'(self.first_name, self.last_name)'