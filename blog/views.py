from datetime import datetime
from pickle import GET
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import About, Profile, blogadd, usersave
from .forms import *
from django.contrib import messages
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    data1 = blogadd.objects.first()
    data = blogadd.objects.all()
    paginator = Paginator(data,2,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method=='GET':
        search_input = request.GET.get('search-area')
        if search_input:
            page_obj = blogadd.objects.filter(blog_title__icontains = search_input)
                
        else:
            search_input= ''

    return render(request,'blog/index.html',{'data':page_obj, 'data1':data1,'search_input':search_input})

def home(request):
    
    if request.method=="POST":
        form = BlogAddForm(request.POST, request.FILES)
        if form.is_valid():
            adform = form.save(commit=False)
            adform.date_blog = datetime.now()
            adform.save()
            return redirect('home')
            
    else:
        form = BlogAddForm()
       
    return render(request,'blog/home.html',{'form':form})


def about(request):
    about = About.objects.all()

    return render(request,'blog/about.html',{'about':about})

def contact(request):
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            client_name = form['firstname'].value()
            client_email = form['email'].value()
            client_message =  form['message'].value()
                # if ContactForm['firstname']!
            subject = 'Inquiry'
            message = 'There has been Inquiry from   ' + client_name +'.  From Email: ' + client_email +'. Message:' + client_message + '.  Sign into the admin panel for more'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = (client_email,)
            send_mail(subject,message,email_from,recipient_list)

            form.save()
            return redirect('contact')  

    else:
        form=ContactForm()

    return render(request,'blog/contact.html',{'form':form})









def userdetail(request):
    if request.method == "POST":
        form = UserdetailForm(request.POST)
        print(form['password'].value())
        if form.is_valid():
            # if ContactForm['firstname']!
        
            if form['password'].value()!=form['cpassword'].value():
                    messages.success(request, ' Password and Confirm Password does not match.')
                    return redirect('signup')
                
            elif User.objects.filter(username = form['user'].value()).first():
                    messages.success(request, ' Username is taken.')
                    return redirect('signup')
            elif User.objects.filter(email = form['email'].value()).first():
                    messages.success(request, ' email is taken.')
                    return redirect('signup')

            


            user_obj = User.objects.create_user(username = form['user'].value(), email=form['email'].value(), password=form['password'].value())
            user_obj.save()
            

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user= user_obj, auth_token = auth_token)
            profile_obj.save()

            sent_mail(form['email'].value(), auth_token)
            
       
        form.save()
    return render(request,'blog/token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                 messages.success(request, 'Your account is already verified')
                 return redirect('login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)

def login(request):
    form = LoginForm(request.POST)
    return render(request,'blog/login.html',{'form': form})


def signup(request):
    form = UserdetailForm(request.POST)
    return render(request,'blog/signup.html',{'form': form})

def error(request):
    return render(request,'error.html')

def sent_mail(email,token):
    subject = 'Your account need to be verified.'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8080/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message, email_from, recipient_list)

def logout(request):
    django_logout(request)
    return redirect('/')

def login1(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

           
            user_obj =  User.objects.filter(username=form['username'].value()).first()
        
            if user_obj is None:
                messages.success(request,'Wrong username')
                return redirect('login')

            profile_obj = Profile.objects.filter(user = user_obj).first()

            if not profile_obj.is_verified:
                messages.success(request,'Profile not verified.')
                return redirect('login')

            user = authenticate(request,username=form['username'].value(),password=form['password'].value())
            if user is None:
                messages.success(request,'Wrong Password')
                return redirect('login')
            django_login(request, user)
            return HttpResponseRedirect('/')
    
               
    return render(request,'blog/home.html',{})
    
def profile(request):
    prof = usersave.objects.all()
    form = UpdateForm(request.GET,request)
    return render(request,'blog/uprofile.html',{'prof':prof,'form':form})

def uprofile(request):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():

        # firstname = request.POST['fname']
        # midname = request.POST['mname']
        # lastname = request.POST['lname']
        # number = request.POST['phone']
        # username = request.POST['username']
            id = usersave.objects.only('id').get(user=form['user'].value()).id
            
            usersave.objects.filter(id = id).update(first=form['first'].value(), middle=form['middle'].value(), last=form['last'].value(),phoneno=form['phoneno'].value())
        

            prof = usersave.objects.all()

    return render(request,'blog/uprofile.html',{'prof':prof,'form':form})
    
def forgot(request):
    
    return render(request,'blog/fPassword.html')


def fpassword(request):

    if request.method == 'POST':
        
        user1 = request.POST.get('user1')
         
        request.session['username']=user1   
         
        if User.objects.filter(username = user1).first():
                email = User.objects.only('email').get(username=user1).email
                subject = 'Forgot Password of the Account.'
                message = f'Hi paste the link to change password of your account http://127.0.0.1:8080/forpassword'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject,message, email_from, recipient_list)
                messages.success(request,"We've emailed you instructions for setting your password.")
            
        else: 
            messages.success(request,'Wrong email address')
      
    return render(request,'blog/fPassword.html',{'user1':user1})

def forpassword(request):

    return render(request,'blog/forpassword.html')

def pass1(request):
    
    if request.method == 'POST':
        
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        user1 = request.session['username']
        
        id = usersave.objects.only('id').get(user=user1).id
        user_obj = User.objects.only('id').get(username=user1)
        if password!=cpassword:
            messages.success(request, ' Password and Confirm Password does not match.')
            return redirect('forpassword')
            
        if User.objects.filter(username = user1).first():
                        user_obj.set_password(password)
                        user_obj.save()
                        usersave.objects.filter(id=id).update(password=password,cpassword=cpassword)

        else:
                    return render(request,'/pass1')
        
       
    return redirect('login')