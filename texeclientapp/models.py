from django.db import models
from datetime import datetime,date, timedelta
# Create your models here.

class registration(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    number = models.CharField(max_length=250, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    profile = models.ImageField(upload_to='images/propic',null=True, blank=True, default="static\images\static_image\icon.svg")
    joindate = models.DateField(null=True, default=date.today())
    last_login = models.DateTimeField(null=True, blank=True)  
    status =models.CharField(max_length = 255,blank=True,null=True, default="active")
    addres =  models.TextField(blank=True,null=True)
    role = models.CharField(max_length=255,blank=True,null=True)
    dob=models.DateField(null=True,)
    def get_email_field_name(self):
        return 'email'

class banner(models.Model):
    top_banner = models.ImageField(upload_to='images/banner',null=True, blank=True)
    top_link = models.CharField(max_length=250, null=True, blank=True)
    middle_banner = models.ImageField(upload_to='images/banner',null=True, blank=True)
    middle_link = models.CharField(max_length=250, null=True, blank=True)
    bottom_banner1 = models.ImageField(upload_to='images/banner',null=True, blank=True)
    bottom_link1 = models.CharField(max_length=250, null=True, blank=True)
    bottom_banner2 = models.ImageField(upload_to='images/banner',null=True, blank=True)
    bottom_link2 = models.CharField(max_length=250, null=True, blank=True)


class category(models.Model):
    category_name=  models.CharField(max_length=255,blank=True,null=True)
    def _str_(self):
        return self.category_name

class sub_category(models.Model):
    subcategory=  models.CharField(max_length=255,blank=True,null=True)
    category=models.ForeignKey(category, on_delete=models.SET_NULL, null=True, blank=True)