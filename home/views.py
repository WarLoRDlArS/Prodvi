from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(login_url='users:login')
def index(request):
    print("came here")
    return render(request, 'home/index.html')
