from django.shortcuts import render
from datetime import date
from django.contrib import messages
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect 

from .models import *
from users.models import Users

from .forms import NoticeForm, FeedbackForm


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
        current_user = Users.objects.get(pid=request.user.pid)  
        employee = Employee.objects.filter(user = current_user).first()
        role = 'Manager' if employee and employee.is_manager else 'Employee'
        doj = employee.doj if employee and employee.doj else 'Not available'

    context = {
            'user_role': role,  # Check if role exists
            'employee': employee,
            'doj':'doj',
        }

    return render(request, 'home/profile.html',context=context)


@login_required(login_url='users:login')
def createfeedbackform(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.status = 'fresh'
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

            # Redirect to assign form template after creation
            return redirect('home:assign_form_to_group', form_id=form_instance.form_id)  # Update the URL name as needed
    else:
        form = FeedbackForm()

    return render(request, 'home/createFormTemplate.html', {'form': form})


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


@login_required(login_url='users:login')
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        new_group = Group(name=group_name)
        new_group.save()
        # Add manager to the group
        new_group.managers.add(request.user.employee.managerid)  # Assuming the manager is logged in
        return redirect('home:group_list')

    return render(request, 'create_group.html')

@login_required(login_url='users:login')
def group_list(request):
    groups = Group.objects.filter(managers=request.user.employee.managerid)
    return render(request, 'home/group_list.html', {'groups': groups})


@login_required(login_url='users:login')
def assign_form_to_group(request, form_id):
    form = Forms.objects.get(form_id=form_id)
    assigned_users = []
    
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        pid_list = request.POST.get('pids', '').split(',')

        # Assign form to group if selected
        if group_id:
            group = Group.objects.get(id=group_id)
            FormAssignedByTo.objects.create(
                manager=request.user.employee.managerid,
                form=form,
                group=group,
                assign_date=date.today()
            )

        # Assign form to users based on PIDs
        for pid in pid_list:
            pid = pid.strip()
            try:
                user = Users.objects.get(pid=pid)
                FormAssignedByTo.objects.create(
                    manager=request.user.employee.managerid,  # Ensure this is correct
                    form=form,
                    employee=user.employee,
                    assign_date=date.today()
                )
                assigned_users.append(user)
            except Users.DoesNotExist:
                continue

        return redirect('home:index')

    # Fetch available groups
    groups = Group.objects.filter(managers=request.user.employee.managerid)
    return render(request, 'home/assign_form.html', {'form': form, 'groups': groups, 'assigned_users': assigned_users})
@login_required(login_url='users:login')
def edit_profile(request):
    current_user = request.user
    employee = Employee.objects.get(user=current_user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Update user details
        current_user.username = username
        current_user.email = email
        current_user.save()

        # Update employee name
        employee.empname = username
        employee.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('home:userProfile')  # Redirect to profile page after saving
    
    context = {
        'employee': employee,
         'current_user': current_user,
    }
    return render(request, 'home/edit_profile.html', context)