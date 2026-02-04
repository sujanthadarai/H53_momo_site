import re
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileForm
from .models import Profile
from payments.models import Order

# Create your views here.
def register(request):
    if request.method == 'POST':
        fname=request.POST['first_name'] #sujan
        lname=request.POST['last_name'] #thadarai
        username=request.POST['username'] #sujan710
        email=request.POST['email'] #sujan@gmail.com
        password=request.POST['password'] #abc
        password1=request.POST['password1'] #abc
        
        if password == password1:
            
            if User.objects.filter(username=username).exists():
                messages.error(request,"This username is already register !!!!")
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request,"This email is already register !!!!")
                return redirect('register')
            
            if not re.search(r'[A-Z]',password):
                messages.error(request,"password must contain at least one upper character !!!")
                return redirect("register")
            if not re.search(r'\d',password):
                messages.error(request,"password must contain at least one  digit !!!")
                return redirect("register") #Ramm710@
            
            try:
                validate_password(password)
                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,"your account is successfully register")
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
                return redirect('register')
        else:
            messages.error(request,"your password and confirm password doesnot match !!!")
            return redirect('register')
            
        
    return render(request,'accounts/register.html')

def log_in(request):
    if request.method =='POST':
        username=request.POST.get("username") #sujan710
        password=request.POST.get("password") #Ramm710@
        remember_me=request.POST.get("remember_me") #on or None
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register yet!!!")
            return redirect("log_in")
        
        user=authenticate(username=username,password=password) #None
        
        if user is not None:
            login(request,user)
            
            if remember_me:
                request.session.set_expiry(1200000)
            else:
                request.session.set_expiry(0)
                
            
            next=request.POST.get("next","") #/about/
            return redirect(next if next else "index")
        else:
            messages.error(request,"password invalid!!!")
            return redirect("log_in")

    next=request.GET.get("next","")
       
    return render(request,'accounts/login.html',{'next':next})


    

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url="log_in")
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_out')
    
    
    return render(request,'accounts/password_change.html',{'form':form})

@login_required(login_url="log_in")
def profile_dashboard(request):
    return render(request,'profile/dashboard.html')

@login_required(login_url="log_in")
def profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(instance=profile)
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request,'profile/profile.html',{'form':form})

@login_required(login_url="log_in")
def my_order(request):
    myorder=Order.objects.filter(user=request.user)
    return render(request,'profile/my_order.html',{'myorder':myorder})