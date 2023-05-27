from email.policy import default
from pyexpat import model
from django import forms
from django.forms import ModelForm
from main.models import Complaint, Notice, Service, Visitor, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

class EditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email', 'age', 'flat_no', 'phone_number', 'status','photo']
    
    ch = (
        ("r", "Resident"),
        ("s", "Staff"),
        ("a", "Superuser")
    )
    name = forms.CharField()
    age = forms.IntegerField()
    email = forms.EmailField()
    flat_no = forms.CharField()
    photo = forms.ImageField(required=False)
    phone_number = forms.IntegerField()
    status = forms.ChoiceField(choices=ch, required=False)

class EditNoticeForm(ModelForm):
    class Meta:
        model = Notice
        fields = ['header_notice','details_notice', 'showflag']
    header_notice = forms.CharField(required=True)
    details_notice = forms.CharField(
        required=False,
        widget=forms.Textarea)
    ch = (("y", "Show"), ("n", "Hide"))    
    showflag = forms.ChoiceField(choices=ch)

class ResolveForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['resolve_msg']
    resolve_msg = forms.CharField(
        required=True,
        widget=forms.Textarea)