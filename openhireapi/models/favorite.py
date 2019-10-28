from django.db import models
from .job import Job
from django.contrib.auth.models import User

class Favorite(models.Model):
    '''
    job: foreign key of job id.
    user: foreign key of user id.
    '''

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)