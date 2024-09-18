from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect 


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
    context = {}
    return render(request, 'home/profile.html',context=context)