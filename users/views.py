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


def index(request):
    return HttpResponse("Hello To Prodvi")

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
        
        login(request, user)
        return redirect(request, 'users:index')

    return render(request, 'users/login.html')