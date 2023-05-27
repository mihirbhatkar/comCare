import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from requests import get
from main.forms import NewUserForm, ComplaintForm, NoticeForm, ServiceForm, VisitorForm, otpForm
from main.models import MainPage
from .models import Complaint, MainPage, Notice, Staff, Profile, Service, Bills, Visitor
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
import os
from twilio.rest import Client
import random
import http.client
import pytz
import razorpay
from django.views.decorators.csrf import csrf_exempt


def homepage(request):
    if request.user.is_authenticated:
        # for u in User.objects.all():
        #     if u.username=='Sachin':
        #         prof = Profile.objects.get(user = u)
        #         u.is_staff
        #         u.save()
        #         prof.status='s'
        #         prof.save()
        #for displaying latest notice on noticeboard:
        max = Notice.objects.get(id = 1)
        utc=pytz.UTC
        maxtime = max.publish_dt.replace(tzinfo=utc)
        for notice in Notice.objects.all():
            noticetime = notice.publish_dt.replace(tzinfo = utc)
            maxtime = max.publish_dt.replace(tzinfo=utc)
            if notice.showflag == 'y':
                if noticetime > maxtime:
                    newestnotice = notice
                    max = notice
                else:
                    newestnotice = max 
        
        #for displaying latest notification
        max = Complaint.objects.filter(complaint_user = request.user)
        newestc=[]
        if max:
            maxi = max[0]
            user = request.user
            utc=pytz.UTC
            newestc = []
            if maxi.status == 'y':
                maxitime = maxi.resolve_time.replace(tzinfo=utc)
                if user.is_authenticated:
                    for c in Complaint.objects.filter(complaint_user = request.user):
                        if c.status == 'y':
                            ctime = c.resolve_time.replace(tzinfo = utc)
                            maxitime = maxi.resolve_time.replace(tzinfo=utc)
                            if ctime > maxitime:
                                newestc = c
                                maxi = c   
                            else:
                                newestc = maxi
        #for displaying the latest bill for that user
        if request.user.username == 'admin':
        
            newestc = []
            billsend=[]
        else:

            max = Bills.objects.filter(user = request.user)
            billsend=[]
            if max:
                for b in max:
                    x = b.bill_id
                maxi = Bills.objects.get(bill_id = x)
                user = request.user
                utc=pytz.UTC
                maxitime = maxi.publish_date.replace(tzinfo=utc)
                if user.is_authenticated:
                    for bill in Bills.objects.filter(user = request.user):
                        if bill.status == 'n':
                            billtime = bill.publish_date.replace(tzinfo=utc)
                            maxitime = maxi.publish_date.replace(tzinfo=utc)
                            if billtime>maxitime:
                                billsend = billtime
                                maxi = billtime
                            else:
                                billsend = maxi    
        
        return render(request=request,
                    template_name='main/home.html',
                    context={'notice':newestnotice, 'complaint':newestc, 'bill':billsend, 'iprofile':Profile.objects.all()})
    else:
        return redirect('main:login')


def register(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New Account Created!: {username}')
            login(request, user)
            messages.info(request, f'You are now logged in as: {username}')
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request, "main/register.html", context={'form': form, 'iprofile':Profile.objects.all()})


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return render(request,"main/home.html")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in')
                return redirect('main:homepage')
            else:
                messages.error(request, f'Invalid username or password')
        else:
            messages.error(request, f'Invalid username or password')

    form = AuthenticationForm()
    return render(request, "main/login.html", {'form': form})


def noticeboard(request):
    
    utc=pytz.UTC
    noticelist = []
    current = datetime.datetime.now()
    currenttime = current.replace(tzinfo=utc)
    for notice in Notice.objects.all():
        noticetime = notice.showtill.replace(tzinfo=utc)
        if notice.showflag == 'y':
            if noticetime >= currenttime:
                noticelist.append(notice)
            else:
                if notice.showflag == 'y':
                    noticelist.append(notice)
                else:
                    notice.showflag = 'n'
    
    messages.info(request, 'You are viewing the Notice Board!')
    return render(request, "main/noticeboard.html", {'noticeboard': noticelist, 'iprofile':Profile.objects.all()})

def notif(request):
    complaintlist=[]
    user = request.user
    for c in Complaint.objects.filter(complaint_user = user):
        print(c)
        if c.status == 'y':
            complaintlist.append(c)
    return render(request, 'main/notif.html', {'complaint': complaintlist, 'iprofile':Profile.objects.all()})

def complaint(request):
    if request.method == 'POST':         
        form = ComplaintForm(request.POST)
        if form.is_valid():
            
            comp = User.objects.get(username = request.user.username)
            # u = User.objects.all()
            
            u1 = request.user.username
            n1 = Profile.objects.get(user = request.user)
            
            newdate = datetime.datetime.now()
            h1 = form.cleaned_data.get('subject')
            h2 = form.cleaned_data.get('content')
            status = 'n'

            newcomp = Complaint(subject = h1, content = h2,flat_no =n1.flat_no, complaint_user = comp, date = newdate, username = u1, name=n1.name, status = status )
            newcomp.save()
            messages.info(request, 'Complaint registered successfully!')
            return redirect('main:homepage')

    return render(request, "main/complaint.html", context={'form': ComplaintForm(), 'iprofile':Profile.objects.all()})    


def staff(request):
    staff = Staff.objects.all()
    return render(request, "main/staff.html", context={'staff': staff, 'iprofile':Profile.objects.all()})


def makenotice(request):
    note = Notice()
    if request.method == 'GET':
        return render(request, "main/makenotice.html", context={'form': NoticeForm()})
    else:
        form = NoticeForm(request.POST)
        newnotice = form.save(commit=False)
        newnotice.user = request.user

        subject = newnotice.header_notice
        message = newnotice.details_notice
        from_email = settings.EMAIL_HOST_USER
        recievers = []
        for user1 in Profile.objects.all():
            recievers.append(user1.email)
        emailsending = EmailMessage(subject, message, from_email, recievers)
        emailsending.send()

        newnotice.save()
        messages.info(request, 'Notice made successfully!')
        return redirect('main:homepage')

def service(request):
    if request.method == 'GET':
        return render(request, "main/service.html", context={'form': ServiceForm(), 'iprofile':Profile.objects.all()})
    else:
        form = ServiceForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user = request.user)
            msg = form.cleaned_data.get('service_details')
            sname = form.cleaned_data.get('service_name')
            if sname == '1':
                subject = 'Request from '+ profile.name + ' --- flat number: '+ profile.flat_no
                message = msg
                from_email = settings.EMAIL_HOST_USER
                recievers = ['mihirbhatkar87@gmail.com']
                emailsending = EmailMessage(subject, message, from_email, recievers)
                emailsending.send()
            elif sname == '2':
                subject = 'Request from '+ profile.name + ' --- flat number: '+ profile.flat_no
                message = msg
                from_email = settings.EMAIL_HOST_USER
                recievers = ['21rihim@gmail.com']
                emailsending = EmailMessage(subject, message, from_email, recievers)
                emailsending.send()
            elif sname == '3':
                subject = 'Request from '+ profile.name + ' --- flat number: '+ profile.flat_no
                message = msg
                from_email = settings.EMAIL_HOST_USER
                recievers = ['nishchayrajpal8@gmail.com']
                emailsending = EmailMessage(subject, message, from_email, recievers)
                emailsending.send()
            else:
                print('fail')
        messages.info(request, 'Service has been notified of your request.')
        return redirect('main:homepage')




def test(request):
    obj = Service.objects.all()
    v1 = obj[0].service_name
    v2 = obj[1].service_name
    v3 = obj[2].service_name
    return render(request, 'main/test.html', context={'v1':v1, 'v2':v2, 'v3':v3})

def viewbill(request, bill_id):

    bill = model_to_dict(Bills.objects.get(pk = bill_id))

    username = request.user.get_username()
    for user1 in Profile.objects.all():
        if username == user1.user.username:
            prof = user1

    total = bill['repairs_maintenance_charges'] + bill['society_service_charges'] + bill['charity_charges'] + bill['sinking_fund_charges'] + bill['parking_charges']
    final = total + bill['previous_dues']

    context={'bill':bill, 'profile':prof, 'total':total, 'final':final, 'bill_id': bill_id, 'iprofile':Profile.objects.all()}

    return render(request, 'main/viewbill.html', context )


def searchbill(request):
    user = request.user
   
    utc=pytz.UTC
    duelist=[]
    pendinglist = []
    paidlist = []
    current = datetime.datetime.now()
    currenttime = current.replace(tzinfo=utc)
    bills = Bills.objects.filter(user = user)
    for b in bills:
        if b.status == 'n':
            billtime = b.due_date.replace(tzinfo=utc)
            if billtime>=currenttime:
                duelist.append(b)
            elif billtime<currenttime:
                pendinglist.append(b)
        elif b.status == 'y':
            paidlist.append(b)        

    if duelist or paidlist or pendinglist:
        # messages.info(request, 'You are viewing your Bills')
        return render(request, 'main/searchbill.html', context={'due':duelist,'paid':paidlist, 'pending': pendinglist, 'iprofile':Profile.objects.all()})

    else:
        return render(request, 'main/nobills.html')    
    

def addvisitor(request):
    if request.method == 'GET':
        return render(request, "main/addvisitor.html", context={'form': VisitorForm()})
    else:
        form = VisitorForm(request.POST)
        global newvisitor
        newvisitor = form.save(commit=False)
        newvisitor.user = request.user
        phone_no = newvisitor.visitor_phone
        
        check_flat = Profile.objects.filter(flat_no = newvisitor.visiting_flat).first()
        if check_flat:
            print('Testing')
        else:
            
            messages.error(request,'No such flat exists')
            return redirect('main:homepage')
        
        global otp
        otp = str(random.randint(1000, 9999))
        vlist = {'phone_no':phone_no, 'otp':otp}
        
        
        sms(phone_no, otp)
        request.session['phone_no'] = phone_no
        return redirect('main:otpfunc')

    

def otpfunc(request):
    mobile = request.session['phone_no']
    form = otpForm(request.POST)
    context = {'mobile':mobile, 'form':otpForm()}
    if request.method == 'GET':
        return render(request,'main/visitorotp.html', context)  
    else:
        otpnew = request.POST.get('otp')
        print(otp)
        print(otpnew)
        if otpnew == otp:
            newvisitor.save()
            messages.info(request, 'Visitor registered successfully!')
            return redirect('sec:ahome')
        else:
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

def visitor(request):
    messages.info(request, 'You are viewing the Visitor Log')
    return render(request, "main/visitor.html", context={'visit': Visitor.objects.all, 'iprofile':Profile.objects.all()})
@csrf_exempt
def pay(request, bill_id):
    
    bill = model_to_dict(Bills.objects.get(pk = bill_id))

    username = request.user.get_username()
    for user1 in Profile.objects.all():
        if username == user1.user.username:
            prof = user1

    total = bill['repairs_maintenance_charges'] + bill['society_service_charges'] + bill['charity_charges'] + bill['sinking_fund_charges'] + bill['parking_charges']
    final = total + bill['previous_dues']

    context={'idbill':bill_id, 'bill':bill, 'profile':prof, 'total':total, 'final':final, 'finalP': final*100, 'iprofile':Profile.objects.all()}

    if request.method == 'POST':
        print(5)
        razorpay_client = razorpay.Client(auth=("rzp_test_CK8AWrEy84pP7i", "UNfgBNxADdlf1rb5rmU4UyPx"))   
        data = { "amount": final*100, "currency": "INR", "receipt": "order_rcptid_11", 'payment_capture': '1'}
        razorpay_order = razorpay_client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']
    return render(request, 'main/pay.html', context)

@csrf_exempt
def success(request, bill_id):
    bill = get_object_or_404(Bills, pk=bill_id)
    bill.status = 'y'
    bill.payment_time = datetime.datetime.now()
    bill.save()

    return render(request, "main/psuccess.html",{'iprofile':Profile.objects.all()})

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'sec/psuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
