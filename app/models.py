from django.db import models
from user_auth.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, datetime 
from django.core.validators import RegexValidator   
# Create your models here.

class Job(models.Model):

    user = models.ForeignKey(User_data, on_delete=models.CASCADE, null=True)
    job_name = models.CharField(max_length=1000, validators=[RegexValidator(regex=r'^[a-zA-Z]+$',message='Field must contain only alphabetical characters.',code='invalid_field')])
    job_location = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    contact = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{10}$',message="Contact Field must contain only 10 digits",code='invalid_field')])
    pin_code = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{1,10}$',
        message="Field must contain only digits",code='invalid_field')])
    budget = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(500)])
    def __str__(self):
        return str(self.job_name) + " " +  str(self.budget)+ " " +  str(self.id)


class BidForJob(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    bid_date = models.DateField(default=date.today, null=True)
    job_biding_price = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(500)])
    confirm_job = models.BooleanField(default=False)
    job_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.service_provider)+" - "+str(self.job)+" - "+str(self.job_biding_price)

class UserFeedback(models.Model):
    user = models.ForeignKey(User_data, on_delete=models.CASCADE, null=True)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    feedback = models.CharField(max_length=1000, null=True)
    ratings = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    def __str__(self):
        return str(self.user)+" - "+str(self.job)