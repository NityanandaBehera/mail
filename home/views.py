from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from .models import *
from home.models import profile
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

def home(request):
 
    return render(request,'base.html')
@login_required(login_url="/")   
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')
        
        
        profile_obj = profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')
        
        login(request , user)
        return redirect(request,'login.html')

    return render(request , 'login.html')
    return render(request,'login.html')
def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
               messages.success(request, 'username is taken.')
               return redirect('/register')
               
            if User.objects.filter(email=email).first():
               messages.success(request, 'email is already exist.')
               return redirect('/register')
            user_obj =User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save() 
            auth_token=str(uuid.uuid4()) 
            profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)  
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/send_mail')
        except Exception as e:
            print(e)

        
    return render(request,'register.html')



def sucess(request):
 return render(request,'sucess.html')

def send_mail(request):
    return render(request,'send_mail.html')    



def verify(request , auth_token):
    try:
        profile_obj = profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/send_mail')

def error_page(request):
    return  render(request , 'error.html')
def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{send_mail}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )