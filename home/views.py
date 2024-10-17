from django.shortcuts import render,get_object_or_404
from datetime import date
from django.contrib import messages
from django.db import transaction

# Create your views here.
from django.template import TemplateDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect 
from django.utils import timezone  # Import the timezone module

from django.db.models import Q


from .models import *
from users.models import Users

from .forms import NoticeForm, FeedbackForm 

 
@login_required(login_url='users:login')
def index(request):
    try:
        # Get the current employee
        employee = Employee.objects.get(user=request.user)

        # Fetch the top 5 new (unacknowledged) notices for the employee
        new_notices = NoticeStatus.objects.filter(employee=employee, acknowledged=False).order_by('-notice__posted_on')[:5]

        # If there are no new notices, fetch the latest assigned notices
        if not new_notices.exists():
            new_notices = NoticeStatus.objects.filter(employee=employee).order_by('-notice__posted_on')[:5]

        # Fetch the top 5 assigned forms for the employee
        assigned_forms = FormAssignedByTo.objects.filter(employee=employee).order_by('-assign_date')[:5]

        # Fetching forms and determining if they are filled
        latest_forms = []
        for assigned_form in assigned_forms:
            form_info = {
                'form': assigned_form.form,
                'has_filled': assigned_form.has_filled
            }
            latest_forms.append(form_info)

        # Fetch memos (assuming you have a `Memo` model), if not you can skip this part
        # latest_memos = Memo.objects.order_by('-created_at')[:5] if Memo.objects.exists() else None

        context = {
            'new_notices': new_notices, 
            'latest_forms': latest_forms,
            # 'latest_memos': latest_memos,
        } 

        return render(request, 'home/index.html', context)
    except Employee.DoesNotExist:
        # Handle the case where the employee does not exist
        return render(request, 'users/landing_page.html')



@login_required(login_url='users:login')
def logout_link(request):
    logout(request)
    return redirect('users:login')


@login_required(login_url='users:login')
def user_profile(request): 

    return render(request, 'home/profile.html')


@login_required(login_url='users:login')
def edit_profile(request): 
    
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
     
    return render(request, 'home/edit_profile.html')


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
 
    return render(request, 'home/createFormTemplate.html')


@login_required(login_url='users:login')
def NoticeView(request):
    emp = Employee.objects.get(user=request.user)
    is_manager = emp.is_manager

    # Get notices created by the logged-in user or assigned to the logged-in employee
    notices = Notice.objects.filter(
        Q(posted_by=request.user) | Q(noticestatus__employee=emp)
    ).distinct().order_by('-posted_on')

    print(f"User: {request.user.username}, is_manager: {is_manager}")
    return render(request, 'home/notice.html', context={'notices': notices})


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

            # Assign notice to selected group or individual employees (like assigning a form)
            group_id = request.POST.get('group_id')
            pid_list = request.POST.get('pids', '')

            # Assign notice to group members
            if group_id:
                group = Group.objects.get(id=group_id)
                for employee in group.employees.all():
                    NoticeStatus.objects.create(notice=notice, employee=employee)

            # Assign notice to users based on PIDs
            pid_list = [pid.strip() for pid in pid_list.split(',') if pid.strip()]
            for pid in pid_list:
                try:
                    user = Users.objects.get(pid=pid)
                    employee = Employee.objects.get(user=user)
                    NoticeStatus.objects.create(notice=notice, employee=employee)
                except Users.DoesNotExist:
                    continue

            return redirect('home:notice')  # Redirect to the notices page
    else:
        form = NoticeForm()

    groups = Group.objects.filter(managers=currentuseremp.managerid)

    return render(request, 'home/add_notice.html', {'form': form, 'groups': groups})


# TODO
@login_required(login_url='users:login')
def employee_notices(request):
    employee = Employee.objects.get(user=request.user)

    # Get all notices assigned to the employee that are not acknowledged
    new_notices = NoticeStatus.objects.filter(employee=employee, acknowledged=False)

    return render(request, 'home/employee_notices.html', {'new_notices': new_notices})


@login_required(login_url='users:login')
def acknowledge_notice(request, notice_status_id):
    notice_status = NoticeStatus.objects.get(id=notice_status_id, employee__user=request.user)
    notice_status.acknowledged = True
    notice_status.acknowledged_date = timezone.now()
    notice_status.save()

    return redirect('home:employee_notices')


# TODO
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


# TODO
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
        pid_list = request.POST.get('pids', '')

        # Strip any extra whitespace and split by comma
        pid_list = [pid.strip() for pid in pid_list.split(',') if pid.strip()]

        # Assign form to group if selected
        if group_id:
            group = Group.objects.get(id=group_id)
            # Check if the form is already assigned to the group
            if not FormAssignedByTo.objects.filter(manager=request.user.employee.managerid, form=form, group=group).exists():
                FormAssignedByTo.objects.create(
                    manager=request.user.employee.managerid,
                    form=form,
                    group=group,
                    assign_date=date.today()
                )

        # Assign form to users based on PIDs
        current_user = Manager.objects.get(user=request.user)
        for pid in pid_list:
            try:
                user = Users.objects.get(pid=pid)
                # Check if the form is already assigned to the user
                if not FormAssignedByTo.objects.filter(manager=current_user, form=form, employee=user.employee).exists():
                    FormAssignedByTo.objects.create(
                        manager=current_user,
                        form=form,
                        employee=user.employee,
                        assign_date=date.today()
                    )
                    assigned_users.append(user)
            except Users.DoesNotExist:
                print(f"Error assigning form to {pid}")

        return redirect('home:index')

    # Fetch available groups
    groups = Group.objects.filter(managers=request.user.employee.managerid)
    return render(request, 'home/assign_form.html', {'form': form, 'groups': groups, 'assigned_users': assigned_users})

@login_required(login_url='users:login')
def view_forms(request):
    forms = Forms.objects.all()  # Get all forms
    return render(request, 'home/view_forms.html', context={'forms': forms})


@login_required(login_url='users:login')
def assigned_forms(request):
    # Get the employee associated with the logged-in user
    employee = get_object_or_404(Employee, user=request.user)

    # Fetch all forms assigned to this employee
    assigned_forms = FormAssignedByTo.objects.filter(employee=employee).select_related('form')

    # Update form status if the employee has viewed the form
    for assignment in assigned_forms:
        if not assignment.has_viewed:
            assignment.has_viewed = True
            assignment.form.status = 'pending'  # Update status to 'pending'
            assignment.save()  # Save changes

    return render(request, 'home/assigned_forms.html', {'assigned_forms': assigned_forms})

@login_required(login_url='users:login')
def fill_feedback_form(request, form_id):
    # Fetch the form based on the form_id
    form_instance = Forms.objects.get(form_id=form_id)

    # Ensure the logged-in employee has access to this form
    employee = Employee.objects.get(user=request.user)
    assignment = FormAssignedByTo.objects.filter(form=form_instance, employee=employee).first()

    if not assignment:
        messages.error(request, "You do not have permission to fill this form.")
        return redirect('home:index')

    questions = Questions.objects.filter(form=form_instance)

    if request.method == 'POST':
        for question in questions:
            answer_text = request.POST.get(f'question_{question.question_id}')
            if answer_text:
                QuestionAnswers.objects.create(
                    question=question,
                    user=request.user,
                    answer_text=answer_text
                )
        
        # Create a FilledForm entry
        FilledForm.objects.create(
            form=form_instance,
            employee=employee
        )

        # Remove the assignment and update the form status
        assignment.delete()
        form_instance.status = 'finished'
        form_instance.save()

        messages.success(request, "Your responses have been submitted successfully!")
        return redirect('home:index')

    return render(request, 'home/fill_feedback_form.html', {
        'form': form_instance,
        'questions': questions
    })

@login_required(login_url='users:login')
def filled_forms(request):
    employee = Employee.objects.get(user=request.user)
    filled_forms = FilledForm.objects.filter(employee=employee).select_related('form')

    return render(request, 'home/filled_forms.html', {'filled_forms': filled_forms})
