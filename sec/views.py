from xml.parsers.expat import model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from main.forms import NewUserForm, ComplaintForm, NoticeForm, ServiceForm, VisitorForm, BillForm, otpForm
from sec.forms import EditForm, EditNoticeForm, ResolveForm
from main.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.db.models import F
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import http.client
import random
from twilio.rest import Client
import pytz


def register(request):

    if request.method == "POST":
        form = NewUserForm(request.POST, request.FILES)


        if form.is_multipart():
            form.save()

            username1 = form.cleaned_data.get('username')
            name1 = form.cleaned_data.get('name')
            email1 = form.cleaned_data.get('email')
            age1 = form.cleaned_data.get('age')
            flat_no1 = form.cleaned_data.get('flat_no')
            phone_number1 = form.cleaned_data.get('phone_number')
            photo1 = form.cleaned_data.get('photo')
      
            new = User.objects.get(username = username1)
            
            passw = form.cleaned_data.get('password1')
            st =form.cleaned_data['status']
            subject = 'Your password for E-Housing Society'
            message = "Your username is: "+username1+'\n Your password is: '+passw
            from_email = settings.EMAIL_HOST_USER
            recievers = [email1]
            emailsending = EmailMessage(subject, message, from_email, recievers)
            emailsending.send()


            print(st)
            if st == 'r':
                newuser = Profile(user=new, email=email1, age=age1, flat_no=flat_no1, phone_number=phone_number1, name=name1, photo=photo1, status = st)
                newuser.save()
            if st == 's':
             
                newuser = Profile(user=new, email=email1, age=age1, flat_no=flat_no1, phone_number=phone_number1, name=name1, photo=photo1, status = st)

                newuser.save()
                us = User.objects.get(username = username1)
                us.is_staff= True
                us.save()
            if st == 'a':
             
                newuser = Profile(user=new, email=email1, age=age1, flat_no=flat_no1, phone_number=phone_number1, name=name1, photo=photo1, status = st)

                newuser.save()
                us = User.objects.get(username = username1)
                us.is_superuser= True
                us.save()  

            # newuser = Profile(user=new, email=email1, age=age1, flat_no=flat_no1, phone_number=phone_number1, name=name1, photo=photo1, status = st)
            # newuser.save()
            messages.success(request, f'New Account Created!: {username1}')
            return redirect("sec:ahome")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            
    form = NewUserForm
    return render(request, "sec/register.html", context={'form': form})


def adminlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('sec:ahome')
            else:
                messages.error(request, f'Invalid username or password')
        else:
            messages.error(request, f'Invalid username or password')

    form = AuthenticationForm()
    return render(request, "sec/login.html", {'form': form})

def hello(request):
    return HttpResponse('Hello!!')

def ahome(request):
    #for updating bills
    
    return render(request, 'sec/ahome.html')

def notices(request):
    return render(request, 'sec/notices.html',{'notice':Notice.objects.all()})

def delnotice(request, n_id):
    vi = get_object_or_404(Notice, pk = n_id)
    vi.delete()
    messages.info(request, 'Notice deleted successfully')
    return render(request, 'sec/ahome.html') 

def shownotice(request, no_id):
    notice =  get_object_or_404(Notice, pk = no_id)
    return render(request, 'sec/shownotice.html', {'notice':notice})

def amakenotice(request):
    note = Notice()
    if request.method == 'GET':
        return render(request, "sec/makenotice.html", context={'form': NoticeForm()})
    else:
        form = NoticeForm(request.POST)
        if form.is_valid():

            header_notice = form.cleaned_data['header_notice']
            details_notice = form.cleaned_data['details_notice']
        
            flag = 'y'
            dt = datetime.datetime.now()
            newnotice = Notice(header_notice = header_notice, details_notice=details_notice, publish_dt = dt, showflag = flag)
            
            subject = newnotice.header_notice
            message = newnotice.details_notice
            from_email = settings.EMAIL_HOST_USER
            recievers = []
            for user1 in Profile.objects.all():
                recievers.append(user1.email)
            emailsending = EmailMessage(subject, message, from_email, recievers)
            emailsending.send()

            newnotice.save()
            messages.success(request, 'Notice made successfully!')
            return redirect('sec:ahome')

def editnotice(request, edit_id):
    notice = get_object_or_404(Notice, pk = edit_id)
    if request.method == 'POST':
        form = EditNoticeForm(request.POST)
        if form.is_valid():
            notice.header_notice = form.cleaned_data['header_notice']
            notice.details_notice = form.cleaned_data['details_notice']
            notice.showflag = form.cleaned_data['showflag']
            notice.save()
            messages.success(request, 'Notice edited successfully!')
            return render(request, 'sec/ahome.html')
    else:
        return render(request, 'sec/editnotice.html', {'notice':notice, 'form':EditNoticeForm})

def residents(request):
 
    return render(request, 'sec/residents.html', {'prof':Profile.objects.all()})     

def showprof(request, profile_id):
    userprofile = get_object_or_404(Profile, pk = profile_id)
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            for user in User.objects.all():
                if user.id == userprofile.user_id:
                    newuser = user
            userprofile.name = form.cleaned_data['name']
            userprofile.email = form.cleaned_data['email']
            userprofile.age = form.cleaned_data['age']
            userprofile.flat_no = form.cleaned_data['flat_no']
            userprofile.phone_number = form.cleaned_data['phone_number']
            if form.cleaned_data['photo'] is not None:
                userprofile.photo = form.cleaned_data['photo']
            
            st = form.cleaned_data['status']
            if st == 'r':
                userprofile.status = st
                userprofile.save()
            if st == 's':
                
                userprofile.status = st
                userprofile.save()
                us = User.objects.get(username = newuser.username )
                us.is_staff= True
                us.save()
            if st == 'a':
             
                userprofile.status = st
                userprofile.save()
                us = User.objects.get(username = newuser.username)
                us.is_superuser= True
                us.save()
            userprofile.save()
            messages.success(request, f'Changes made successfully!')
            return redirect('sec:ahome')
        
    else:
        
        return render(request, 'sec/edituser.html', {'userp': userprofile, 'form':EditForm, 'prof':Profile.objects.all()})

def deleteuser(request, del_id):
    userprof = get_object_or_404(Profile, pk = del_id)
    for user in User.objects.all():
        if user.id == userprof.user_id:
            deluser = user
    userprof.delete()
    deluser.delete()
    messages.success(request, 'User deleted successfully')
    return render(request, 'sec/ahome.html')


def visitor(request):
    messages.info(request, 'You are viewing the Visitor Log')
    return render(request, "sec/visitor.html", context={'visit': Visitor.objects.all})

def addvisitor(request):
    if request.method == 'GET':
        return render(request, "sec/addvisitor.html", context={'form': VisitorForm()})
    else:
        form = VisitorForm(request.POST)
        if form.is_valid():

            visitor_name = form.cleaned_data['visitor_name']
            visitor_phone = form.cleaned_data['visitor_phone']
            visiting_flat= form.cleaned_data['visiting_flat']
            visiting_date = form.cleaned_data['visiting_date']
            visiting_time = form.cleaned_data['visiting_time']
            

            vi = Visitor(visitor_name = visitor_name, visitor_phone= visitor_phone, visiting_flat=visiting_flat, visiting_date=visiting_date,
                visiting_time=visiting_time)
            # newvisitor.user = request.user
            phone_no = visitor_phone
            check_flat = Profile.objects.filter(flat_no = visiting_flat).first()
            if check_flat:
                print(' ')
            else:
                
                messages.error(request,'No such flat exists')
                return redirect('sec:ahome')
            
            global otp
            otp = str(random.randint(1000, 9999))
            
            sms(phone_no, otp)
            
            request.session['phone_no'] = phone_no
            vi.save()
            vi_id = vi.id
            
            return redirect(f'/admin/otpfunc/{vi_id}')


def delvisitor(request, v_id):
    vi = get_object_or_404(Visitor, pk = v_id)
    vi.delete()
    messages.info(request, 'Visitor deleted successfully')
    return render(request, 'sec/ahome.html')     

    
def complaints(request):
    return render(request, 'sec/showcomplaints.html', {'comp':Complaint.objects.all()})    

def opencomplaint(request, c_id):
    complaint =  get_object_or_404(Complaint, pk = c_id)
    return render(request, 'sec/usercomplaint.html', {'com':complaint})

def deletecomplaint(request, co_id):
    ci = get_object_or_404(Complaint, pk = co_id)
    ci.delete()
    messages.info(request, 'Complaint deleted successfully')
    return render(request, 'sec/ahome.html') 


def showbill(request, p_id):
    profile = get_object_or_404(Profile, pk = p_id)
    x = 0 #for checking if user has bills or not
    
    profileusername = profile.user.username
    list = []
    for user1 in Bills.objects.all():
        if profileusername == user1.user.username:
            list.append(user1)
            x=1
    return render(request, 'sec/showbills.html', {'prof': profile, 'bill':list})
    
def billview(request, bill_id, p_id):
    profile = get_object_or_404(Profile, pk = p_id)
    bill = get_object_or_404(Bills, pk = bill_id)
    bill1 = model_to_dict(bill)
    total = bill1['repairs_maintenance_charges'] + bill1['society_service_charges'] + bill1['charity_charges'] + bill1['sinking_fund_charges'] + bill1['parking_charges']
    

    return render(request, 'sec/billview.html', {'profile': profile, 'bill':bill, 'total':total})

def billdelete(request, bill_id):
    bill = get_object_or_404(Bills, pk = bill_id)    
    bill.delete()
    messages.info(request, 'Bill deleted successfully')
    return render(request, 'sec/residents.html')

def createbill(request, pr_id):
    profile = get_object_or_404(Profile, pk = pr_id)
   
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():

            for user in User.objects.all():
                if user.id == profile.user_id:
                    newuser = user
            repairs_maintenance_charges = form.cleaned_data['repairs_maintenance_charges']
            society_service_charges = form.cleaned_data['society_service_charges']
            sinking_fund_charges = form.cleaned_data['sinking_fund_charges']
            parking_charges = form.cleaned_data['parking_charges']
            charity_charges = form.cleaned_data['charity_charges']
            publish_date = datetime.datetime.now()
            due_date = form.cleaned_data['due_date']
            previous_dues = 0
            status = 'n'
            
            bill_id = str(random.randint(1000, 9999)) + profile.flat_no 
            billname = profile.flat_no + '--- Bill ID: '+ str(bill_id)
            newbill = Bills(repairs_maintenance_charges = repairs_maintenance_charges,
                            society_service_charges = society_service_charges,
                            sinking_fund_charges = sinking_fund_charges,
                            parking_charges =parking_charges,
                            charity_charges = charity_charges,
                            previous_dues = previous_dues,
                            publish_date = publish_date,
                            due_date = due_date,
                            user = newuser,
                            flat_no_and_date = billname,
                            status=status,
                            bill_id = bill_id
                            )
            newbill.save()                
            messages.info(request, 'Bill generated successfully')
            return render(request, 'sec/ahome.html')
        
    else:
                
        return render(request, 'sec/billcreate.html', {'profile': profile, 'form':BillForm})

def massbill(request):
   
    if request.method == 'POST':
        form = BillForm(request.POST)
        print("hiii")
        if form.is_valid():
   
            repairs_maintenance_charges = form.cleaned_data['repairs_maintenance_charges']
            society_service_charges = form.cleaned_data['society_service_charges']
            sinking_fund_charges = form.cleaned_data['sinking_fund_charges']
            parking_charges = form.cleaned_data['parking_charges']
            charity_charges = form.cleaned_data['charity_charges']
            publish_date = datetime.datetime.now()
            due_date = form.cleaned_data['due_date']
            previous_dues = 0
            status = 'n'
            
            for user in Profile.objects.all():
                bill_id = str(random.randint(1000, 9999)) + user.flat_no 
                billname = user.flat_no + '--- Bill ID: '+ str(bill_id)
                newbill = Bills(repairs_maintenance_charges = repairs_maintenance_charges,
                                society_service_charges = society_service_charges,
                                sinking_fund_charges = sinking_fund_charges,
                                parking_charges =parking_charges,
                                charity_charges = charity_charges,
                                previous_dues = previous_dues,
                                publish_date = publish_date,
                                due_date = due_date,
                                user = user.user,
                                flat_no_and_date = billname,
                                status = status,
                                bill_id=bill_id
                                )
                newbill.save()                
            messages.success(request, 'Bills created successfully')
            return render(request, 'sec/ahome.html')
        
    else:
                
        return render(request, 'sec/massbill.html', {'form':BillForm})

def otpfunc(request, vi_id):
    mobile = request.session['phone_no']
    visitor = get_object_or_404(Visitor, pk=vi_id)
    form = otpForm(request.POST)
    context = {'mobile':mobile, 'form':otpForm()}
    if request.method == 'GET':
        return render(request,'main/visitorotp.html', context)  
    else:
        otpnew = request.POST.get('otp')
        print(otp)
        print(otpnew)
        if otpnew == otp:
            
            messages.success(request, 'Visitor registered successfully!')
            return render(request,'sec/ahome.html')
            
        else:
            visitor.delete()
            messages.error(request, 'Wrong otp entered!')
            return render(request,'sec/ahome.html', context) 


def sms(mobile, otp):
     
 
    account_sid = 'AC1be04f78c7992d2b8bbe64386ae1a190' 
    auth_token = '713a4a324e58a1994ebe1b2e79820a46' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MG9217aa22b3c308b0a0c298d1aa79ce50', 
                                body=f'The otp is {otp}',      
                                to=f'{mobile}'
                            ) 
    
    print(message.sid)


def send_otp(mobile , otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    print('works')
    authkey = settings.AUTH_KEY
    payload = "{\"Value1\":\"Param1\",\"Value2\":\"Param2\",\"Value3\":\"Param3\"}"
    newmobile = str(mobile)
    newotp = str(otp)
    headers = { 'Content-Type': "application/json" }
    url1 ="https://api.msg91.com/api/v5/otp?otp="+otp+"&message="+"Your%20otp%20is%20"+newotp+"&mobile="+newmobile+"&authkey="+authkey+"&country=+91"
    conn.request("GET",url1, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None        


def resolve(request, c_id):
    complaint = get_object_or_404(Complaint, pk=c_id)
    if request.method == 'POST':
        form = ResolveForm(request.POST)
        if form.is_valid():
            complaint.resolve_msg = form.cleaned_data['resolve_msg']
            complaint.resolve_time = datetime.datetime.now()
            complaint.status = 'y'
            complaint.save()
            # comp = Complaint(resolve_msg = msg, resolve_time = msgtime, status =status)
            # comp.save()
            return render(request, 'sec/ahome.html')

    else:
        return render(request, 'sec/resolve.html', {'form':ResolveForm})        

        
def allbills(request):

    return render(request, 'sec/allbills.html', {'profile':Profile.objects.all()})

def paidbills(request):
    utc=pytz.UTC
    duelist=[]
    pendinglist = []
    paidlist = []
    current = datetime.datetime.now()
    currenttime = current.replace(tzinfo=utc)
    bills = Bills.objects.all()
    for b in bills:
        if b.status == 'n':
            billtime = b.due_date.replace(tzinfo=utc)
            if billtime>=currenttime:
                duelist.append(b)
            elif billtime<currenttime:
                pendinglist.append(b)
        elif b.status == 'y':
            paidlist.append(b)

    for bill in paidlist:
        bill.flat_no_and_date = bill.flat_no_and_date[:4]
        
    return render(request, 'sec/paidbills.html', {'paid':paidlist,'profile':Profile.objects.all()})

def latebills(request):
    utc=pytz.UTC
    duelist=[]
    pendinglist = []
    paidlist = []
    current = datetime.datetime.now()
    currenttime = current.replace(tzinfo=utc)
    bills = Bills.objects.all()
    for b in bills:
        if b.status == 'n':
            billtime = b.due_date.replace(tzinfo=utc)
            if billtime>=currenttime:
                duelist.append(b)
            elif billtime<currenttime:
                pendinglist.append(b)
        elif b.status == 'y':
            paidlist.append(b)

    for bill in pendinglist:
        bill.flat_no_and_date = bill.flat_no_and_date[:4]
        
    return render(request, 'sec/pendingbills.html', {'pending':pendinglist,'profile':Profile.objects.all()})    


def duebills(request):
    utc=pytz.UTC
    duelist=[]
    pendinglist = []
    paidlist = []
    current = datetime.datetime.now()
    currenttime = current.replace(tzinfo=utc)
    bills = Bills.objects.all()
    for b in bills:
        if b.status == 'n':
            billtime = b.due_date.replace(tzinfo=utc)
            if billtime>=currenttime:
                duelist.append(b)
            elif billtime<currenttime:
                pendinglist.append(b)
        elif b.status == 'y':
            paidlist.append(b)

    for bill in duelist:
        bill.flat_no_and_date = bill.flat_no_and_date[:4]        

    return render(request, 'sec/duebills.html', {'due':duelist,'profile':Profile.objects.all()})        