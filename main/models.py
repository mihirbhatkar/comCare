from pydoc import resolve
from tokenize import blank_re
from django.db import models
from django.db.models.fields import CharField, TextField, EmailField, IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from datetime import date, datetime
import datetime
class MainPage(models.Model):
    society_name = CharField(max_length=200)
    society_about = TextField()

    def __str__(self):
        return self.society_name

class Profile(models.Model):
    ch = (
        ("r", "Resident"),
        ("s", "Staff"),
        ("a", "Superuser")
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    age = models.IntegerField(blank=True)
    flat_no = models.CharField(max_length=10)
    phone_number = models.IntegerField()
    photo = models.ImageField(null=True,upload_to='main/images', blank =True)
    status = models.CharField(max_length = 1, null=True, choices=ch)
    def __str__(self):
        return str(self.flat_no+' '+self.name)


class Notice(models.Model):
    ch = (
        ("y", "Show"),
        ("n", "Hide")
    )
    header_notice = CharField(max_length=100)
    details_notice = TextField()
    showtill = models.DateTimeField(blank=True, default=(datetime.datetime.now() + datetime.timedelta(days=1)))
    showflag = models.CharField(max_length=1, blank=True, choices=ch)
    publish_dt = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __str__(self):
        return self.header_notice

class Complaint(models.Model):
    username = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    flat_no = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(null=True)
    subject = models.CharField(null=True, max_length=100)
    content = models.TextField(null=True)
    ch =(("y", "Resolved"), ("n", "Not Resolved"))
    status = models.CharField(max_length=1,null=True, choices=ch)
    resolve_msg = models.TextField(null=True)
    resolve_time = models.DateTimeField(null=True)
    complaint_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.complaint_user)

class Staff(models.Model):
    staff_name = models.CharField(max_length=100)
    staff_email = models.EmailField()
    staff_phone = models.IntegerField()
    designation = models.CharField(max_length=100)
    about = models.TextField(null=True)
    image = models.ImageField(upload_to='main/images')
    def __str__(self):
        return str(self.designation)

class Visitor(models.Model):
    visitor_name = models.CharField(max_length=100)
    visitor_phone =  models.IntegerField()
    visiting_flat = models.CharField(max_length=100)
    visiting_date = models.DateField(default=datetime.date.today)
    visiting_time = models.TimeField(default=datetime.datetime.now)
    def __str__(self):
        return str(self.visitor_name)



class Service(models.Model):
    service_name=models.CharField(max_length=100)
    service_email=models.EmailField(null=True)
    service_details=models.TextField(blank=True)
    def __str__(self):
        return str(self.service_name)


class Bills(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    ch = (("y", "Paid"), ("n", "Pending"))
    status = models.CharField(max_length=1, choices=ch, blank=True)
    payment_time = models.DateTimeField(blank=True, default=datetime.datetime.now)
    bill_id = models.CharField(max_length=100, null=True)
    repairs_maintenance_charges = models.IntegerField()
    society_service_charges = models.IntegerField()
    sinking_fund_charges = models.IntegerField(default=80)
    parking_charges = models.IntegerField(default=100)
    charity_charges = models.IntegerField(default=20)
    previous_dues = models.IntegerField(default=0, null=True)
    publish_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    due_date = models.DateTimeField(blank=True)
    flat_no_and_date = models.CharField(max_length=100)

    def __str__(self):
        return str(self.flat_no_and_date)
