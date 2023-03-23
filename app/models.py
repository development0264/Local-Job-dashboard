from django.db import models
from user_auth.models import User_data
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Job(models.Model):

    job_name = models.CharField(max_length=1000)
    job_location = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    contact = models.CharField(max_length=1000)
    pin_code = models.CharField(max_length=1000)
    budget = models.IntegerField(default=3,validators=[MaxValueValidator(10000), MinValueValidator(500)])
    def __str__(self):
        return str(self.job_name)


class BidForJob(models.Model):
    user = models.ForeignKey(User_data, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    job_biding_price = models.CharField(max_length=1000, null=True)
    confirm_job = models.BooleanField(default=False)
    job_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)+" - "+str(self.job)

class UserFeedback(models.Model):
    user = models.ForeignKey(User_data, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    feedback = models.CharField(max_length=1000, null=True)
    ratings = models.IntegerField(default=3,validators=[MaxValueValidator(5), MinValueValidator(1)])
    def __str__(self):
        return str(self.user)+" - "+str(self.job)

 