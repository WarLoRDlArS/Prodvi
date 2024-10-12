from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect 

from .models import Employee, Manager, Notice
from users.models import Users

from .forms import NoticeForm


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
        employee = Employee.objects.filter(user = current_user[0])[0] 

    context = {'employee': employee, }
    return render(request, 'home/profile.html',context=context)

 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Forms, Questions

@login_required(login_url='users:login')
def createfeedbackform(request):
    if request.method == 'POST':
        print(request.POST)
        # Get the form title from the POST data
        form_title = request.POST.get('title')
        
        # Create and save the Forms instance
        form_instance = Forms(title=form_title, status='fresh')
        form_instance.save()

        # Initialize lists for question texts and types
        questions = []
        for key in request.POST:
            if key.startswith('question_text_'):
                index = key.split('_')[-1]  # Get the question number
                question_text = request.POST.get(key)
                question_type = request.POST.get(f'question_type_{index}')
                questions.append((question_text, question_type))
        
        # Loop through the questions and save them
        for question_text, question_type in questions:
            if question_text:  # Ensure that the question text is not empty
                Questions.objects.create(
                    form=form_instance,
                    question_text=question_text,
                    question_type=question_type
                )

        return redirect('home:index')  # Redirect to a success page or form list

    return render(request, 'home/createFormTemplate.html')


@login_required
def NoticeView(request):
    notices = Notice.objects.all()
    emp = Employee.objects.get(user=request.user)
    is_manager = emp.is_manager

    print(f"User: {request.user.username}, is_manager: {is_manager}")
    return render(request, 'home/notice.html', {
        'notices': notices,
        'is_manager': is_manager,
    })

@login_required(login_url='users:login')
def add_notice(request):
    currentuseremp = Employee.objects.get(user=request.user)
    if not currentuseremp.is_manager:
        return redirect('home:notice')  # Redirect if not a manager

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user  # Set the user who posted the notice
            notice.save()
            return redirect('home:notice')  # Redirect to the notices page
    else:
        form = NoticeForm()
    return render(request, 'home/add_notice.html', {'form': form})
