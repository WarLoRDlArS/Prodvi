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

        if not pid:
            messages.error(request, 'PID is required')
            return redirect('users:login')
        
        if not password:
            messages.error(request, 'Password is required')
            return redirect('users:login')

        if not Users.objects.filter(pid=pid).exists():
            messages.error(request, 'Invalid PID')
            return redirect('users:login')
        
        user = authenticate(request, pid=pid, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            return redirect('users:login')
        
        login(request, user)
        return redirect('home:index')

    return render(request, 'users/login.html')



def landing_page(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    return render(request, 'users/landing_page.html')
 
from django.shortcuts import render, redirect
from django.contrib import messages
from home.models import Users, Employee, Manager  # Ensure you import your models

def signup_page(request):
    if request.method == 'POST': 
        name = request.POST.get('name')
        email = request.POST.get('email')
        pid = request.POST.get('pid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2: 
            messages.error(request, 'Passwords should match.', extra_tags='signup_diff_passwd')
            return redirect('users:signup')

        # Check if PID length is valid
        if len(pid) != 6:
            messages.error(request, 'PID length should be exactly 6.')
            return redirect('users:signup')
        
        # Check if the user already exists
        if Users.objects.filter(pid=pid).exists():
            messages.error(request, 'User already exists.')
            return redirect('users:signup')

        # Determine if the user is a manager
        is_manager = request.POST.get('role') == 'manager' 

        # Try to create the user and associated employee/manager
        try:
            newuser = Users.objects.create(pid=pid, username=name, email=email)
            newuser.set_password(password1)  # Use password1 as it should match password2
            newuser.save()  # Save the user instance first

            # Create the employee instance
            newemp = Employee.objects.create(user=newuser, empid=pid, empname=name, is_manager=is_manager)

            # If the user is a manager, create a manager instance
            if is_manager:
                Manager.objects.create(user=newuser, managerid=pid, is_manager=True)

            # Successful signup
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('users:login')

        except Exception as e:
            # Log the exception message if necessary for debugging
            messages.error(request, 'Sorry! User could not be created. Please try again.')
            return redirect('users:signup')

    # Render the signup page for GET requests
    return render(request, 'users/signup.html')
