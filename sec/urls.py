from pydoc import resolve
from django.conf import settings
from django.urls import path
from main.views import *
from .import views 
app_name='sec'

urlpatterns = [

    path('hello', views.hello, name='hello'),

    path('', views.adminlogin, name='adminlogin'),
    path('ahome', views.ahome, name = 'ahome'),

    path('visitor', views.visitor, name='visitor'),
    path('addvisitor', views.addvisitor, name='addvisitor'),
    path('visitor/<int:v_id>/', views.delvisitor, name='delvisitor'),
    path('otpfunc/<int:vi_id>/', views.otpfunc, name='otpfunc'),

    path('residents', views.residents, name='residents'),
    path('register', views.register, name='register'),
    path('<int:del_id>/', views.deleteuser, name='deleteuser'),
    path('residents/<int:profile_id>/', views.showprof, name='showprof'),
    
    path('amakenotice/', views.amakenotice, name='amakenotice'),
    path('notices', views.notices, name='notices'),
    path('notices/n/<int:no_id>/', views.shownotice, name='shownotice'),
    path('notices/<int:n_id>/', views.delnotice, name='delnotice'),
    path('notices/editnotice/<int:edit_id>', views.editnotice, name='editnotice'),

    path('residents/bills/<int:p_id>/', views.showbill, name ='showbill'),
    path('residents/bills/view/<int:bill_id>/<int:p_id>/', views.billview, name ='billview'),
    path('residents/bills/del/<int:bill_id>/', views.billdelete, name ='billdelete'),
    path('residents/bills/create/<int:pr_id>/', views.createbill, name ='createbill'),
    path('residents/massbill', views.massbill, name='massbill'),
    path('allbills', views.allbills, name='allbills'),
    path('paidbills', views.paidbills, name='paidbills'),
    path('latebills', views.latebills, name='latebills'),
    path('duebills', views.duebills, name='duebills'),

    path('complaints/c/<int:co_id>/', views.deletecomplaint, name='deletecomplaint'),
    path('complaints/<int:c_id>/',views.opencomplaint, name='opencomplaint'),
    path('complaints', views.complaints, name='complaints'),
    path('complaints/resolve/<int:c_id>/', views.resolve, name='resolve')
     
]