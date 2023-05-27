from django.contrib import admin
from django.contrib.admin.helpers import Fieldset
from django.db.models import fields
from django.db import models
from .models import MainPage, Profile, Notice, Complaint, Staff, Service, Bills, Visitor


admin.site.register(Profile)
admin.site.register(Notice)
admin.site.register(Complaint)
admin.site.register(Staff)
admin.site.register(Service)
admin.site.register(Bills)
admin.site.register(Visitor)
