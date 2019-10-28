from django.db import models

class Job(models.Model):
    '''
    title: job title
    description: job description
    city: city where job is located
    state: state where job is located
    application: link to application process
    created_at: date/time job was created
    '''

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    application = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Job")
        verbose_name_plural =("Jobs")


