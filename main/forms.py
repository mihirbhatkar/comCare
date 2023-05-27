from email.policy import default
from django import forms
from django.forms import ModelForm
from .models import Complaint, Notice, Service, Visitor, Bills
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings 
class NewUserForm(UserCreationForm):
    c = (
        ("r", "Resident"),
        ("s", "Staff"),
        ("a", "Superuser")
    )
    email = forms.EmailField(required=True)
    age = forms.IntegerField()
    photo = forms.ImageField()
    flat_no = forms.CharField(max_length=10, required=True)
    phone_number = forms.IntegerField()
    name=forms.CharField(max_length=100)
    status = forms.ChoiceField(choices=c)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", 'name','age', 'flat_no'
                , 'phone_number','photo')
        def save(self, commit=True):
            user =  super(NewUserForm, self).save(commit=False)
            user.name = self.cleaned_data['name']
            user.email = self.cleaned_data['email']
            user.age = self.cleaned_data['age']
            user.flat_no = self.cleaned_data['flat_no']
            user.phone_number = self.cleaned_data['phone_number']
            user.status = self.cleaned_data['status']
            user.photo = self.cleaned_data['photo']

            if commit:
                user.save()
            return user

class otpForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ['otp']
    otp = forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        super(otpForm, self).__init__(*args, **kwargs)
        self.fields['otp'].label = "Enter the OTP:"

class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'content']


    subject = forms.CharField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )


class NoticeForm(ModelForm):
    class Meta:
        model = Notice
        fields = ['header_notice', 'details_notice']

    header_notice = forms.CharField(required=True)
    details_notice = forms.CharField(required=True,widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        self.fields['header_notice'].label = "Specify the subject:"
        self.fields['details_notice'].label = "Enter the content of the notice:"


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['service_name','service_details']

    demo_choice = (
                    ("1", "Electrician"),
                    ("2", "Internet Service Provider"),
                    ("3", "Plumber"),
                  )
    service_name = forms.ChoiceField(choices = demo_choice )
   
    service_details = forms.CharField(required=True,widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
 
        self.fields['service_details'].label = "Specify your request:"


class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ['visitor_name', 'visitor_phone', 'visiting_flat', 'visiting_date', 'visiting_time']


    visitor_name = forms.CharField(max_length=100, required = True)
    visitor_phone =  forms.IntegerField(required = True)
    visiting_flat = forms.CharField(max_length=100, required = True)
    visiting_date = forms.DateField(required = True)
    visiting_time = forms.TimeField(required = True)

class BillForm(ModelForm):
    class Meta:
        model = Bills
        fields = ['repairs_maintenance_charges', 'society_service_charges', 'sinking_fund_charges',
                 'parking_charges', 'charity_charges', 'due_date']
    
    repairs_maintenance_charges = forms.IntegerField()
    society_service_charges = forms.IntegerField()
    sinking_fund_charges = forms.IntegerField()
    parking_charges = forms.IntegerField()
    charity_charges = forms.IntegerField()
    due_date = forms.DateTimeField()