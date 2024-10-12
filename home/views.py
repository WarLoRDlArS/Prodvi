from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect 
from .models import Employee, Manager
from users.models import Users

@login_required(login_url='users:login')
def index(request):
    # print("home:view-index View  : came here")
    return render(request, 'home/index.html')


@login_required(login_url='users:login')
def logout_link(request):
    logout(request)
    return redirect('users:login')


@login_required(login_url='users:login')
def user_profile(request):
    # do all query stuff and all over here
    if request.user.is_authenticated: 
        current_user = Users.objects.filter(pid=request.user.pid) 
        print(current_user)
        employee = Employee.objects.filter(user = current_user[0])[0] 
        print(employee)
    context = {'employee': employee, }
    return render(request, 'home/profile.html',context=context)