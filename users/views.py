from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect 

from .models import Users
from home.models import Employee, Manager


# def index(request):
#     return HttpResponse("Hello To Prodvi")
# above stuff is managed by home

def login_page(request):
    if request.method == "POST": 
        pid = request.POST.get("pid")
        password = request.POST.get("password")

        if not Users.objects.filter(pid=pid).exists():
            messages.error(request, 'Invalid Username')
            return redirect('users:login')
        
        user = authenticate(request, pid=pid, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            return redirect('users:login')
            # print("User is None")
        
        login(request, user)
        # print("Login Successful")
        #  Login is a success
        return redirect('home:index')

        # Test Login
        # pid: 000000
        # password: abc

    return render(request, 'users/login.html')


def landing_page(request):
    return render(request, 'users/landing_page.html')

def signup_page(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        email = request.POST.get("email")
        pid = request.POST.get('pid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            print("Re-Enter password")
            return redirect('users:signup')

        if len(pid) != 6:
            print("PID length should be exactly 6")
            return redirect('users:signup')
        
        userexists = Users.objects.filter(pid = pid)
        if userexists:
            print("User Exists")
            return redirect('users:signup')

        is_manager = True if request.POST.get('role') == 'manager' else False
            
        try:
            newuser = Users.objects.create(pid=pid, username=name, email=email)
            newuser.set_password(password2)
            newemp = Employee.objects.create(user=newuser, empid=pid, empname=name, is_manager=is_manager)
            if is_manager:
                newman = Manager.objects.create.objects.create(user=newuser, managerid=pid, is_manager=True)
                newman.save()
            newemp.save()    
            newuser.save()
            print("User Created Successfully!!")
            return redirect('users:login')
        except(error):
            print(error)
            return redirect('users:signup')

    return render(request, 'users/signup.html')