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
from django.core.exceptions import ValidationError
from django.db.models import Q


from .models import *
from users.models import Users

from .forms import NoticeForm, FeedbackForm 

 
@login_required(login_url='users:login')
def index(request):
    try: 
        employee = Employee.objects.get(user=request.user)
 
        new_notices = NoticeStatus.objects.filter(employee=employee, acknowledged=False).order_by('-notice__posted_on')[:5]
 
        if not new_notices.exists():
            new_notices = NoticeStatus.objects.filter(employee=employee).order_by('-notice__posted_on')[:5]
 
        assigned_forms = FormAssignedByTo.objects.filter(employee=employee).order_by('-assign_date')[:5]
 
        latest_forms = []
        for assigned_form in assigned_forms:
            form_info = {
                'form': assigned_form.form,
                'has_filled': assigned_form.has_filled
            }
            latest_forms.append(form_info)
        # print(latest_forms)
        # Fetch memos (assuming you have a `Memo` model), if not you can skip this part
        # latest_memos = Memo.objects.order_by('-created_at')[:5] if Memo.objects.exists() else None

        context = {
            'new_notices': new_notices, 
            'latest_forms': latest_forms,
            # 'latest_memos': latest_memos,
        } 

        return render(request, 'home/index.html', context)
    except Employee.DoesNotExist: 
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
        
        current_user = request.user
        # Update user details
        current_user.username = username
        current_user.email = email
        current_user.save()

        # Update employee name
        employee = Employee.objects.get(user=current_user)
        employee.empname = username
        employee.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('home:userProfile')  
     
    return render(request, 'home/edit_profile.html')


# TODO Test The below 
@login_required(login_url='users:login')
def createfeedbackform(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.status = 'fresh'
            form_instance.save()
 
            questions = []
            errors = []   

            for key in request.POST:
                if key.startswith('question_text_'):
                    index = key.split('_')[-1]   
                    question_text = request.POST.get(key)
                    question_type = request.POST.get(f'question_type_{index}')
 
                    if not question_text:
                        errors.append(f"Question text for question {index} is required.")

                    min_value = request.POST.get(f'min_value_{index}', None)  # Get min value if provided
                    max_value = request.POST.get(f'max_value_{index}', None)  # Get max value if provided

                    min_value = min_value if min_value else 0
                    max_value = max_value if max_value else 0
 
                    if question_type == 'numeric':
                        try:
                            min_value = float(min_value) if min_value else None
                            max_value = float(max_value) if max_value else None

                            if min_value is not None and max_value is not None and min_value > max_value:
                                errors.append("Min value cannot be greater than max value.")
                        except ValueError:
                            errors.append(f"Non-numeric values entered for min/max values in question {index}.")
 
                    questions.append((question_text, question_type, min_value, max_value))
 
            if errors:
                for error in errors:
                    form.add_error(None, error)
                return render(request, 'home/createFormTemplate.html', {'form': form})
 
            for question_text, question_type, min_value, max_value in questions:
                if question_text: 
                    Questions.objects.create(
                        form=form_instance,
                        question_text=question_text,
                        question_type=question_type,
                        min_value=min_value,  
                        max_value=max_value  
                    )
 
            return redirect('home:assign_form_to_group', form_id=form_instance.form_id)

    else:
        form = FeedbackForm()

    return render(request, 'home/createFormTemplate.html', {'form': form})


@login_required(login_url='users:login')
def NoticeView(request):
    emp = Employee.objects.get(user=request.user)
    is_manager = emp.is_manager
 
    notices = Notice.objects.filter(
        Q(posted_by=request.user) | Q(noticestatus__employee=emp)
    ).distinct().order_by('-posted_on')
 
    return render(request, 'home/notice.html', context={'notices': notices})


@login_required(login_url='users:login')
def add_notice(request):
    currentuseremp = Employee.objects.get(user=request.user)
    if not currentuseremp.is_manager:
        return redirect('home:notice')  

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user   
            notice.save()
 
            group_id = request.POST.get('group_id')
            pid_list = request.POST.get('pids', '')
 
            if group_id:
                group = Group.objects.get(id=group_id)
                for employee in group.employees.all():
                    NoticeStatus.objects.create(notice=notice, employee=employee)
 
            pid_list = [pid.strip() for pid in pid_list.split(',') if pid.strip()]
            for pid in pid_list:
                try:
                    user = Users.objects.get(pid=pid)
                    employee = Employee.objects.get(user=user)
                    NoticeStatus.objects.create(notice=notice, employee=employee)
                except Users.DoesNotExist:
                    continue

            return redirect('home:notice')  
    else:
        form = NoticeForm()

    groups = Group.objects.filter(managers=currentuseremp.managerid)

    return render(request, 'home/add_notice.html', {'form': form, 'groups': groups})


# TODO
@login_required(login_url='users:login')
def employee_notices(request):
    employee = Employee.objects.get(user=request.user)
 
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
         
        new_group.managers.add(request.user.employee.managerid)   
 
        employee_ids = request.POST.getlist('employees')
        for emp_id in employee_ids:
            print(f"empid is {emp_id}")
            employee = Employee.objects.get(empid=emp_id)
            new_group.employees.add(employee)

        messages.success(request, 'Group created successfully!')
        return redirect('home:group_list')  
 
    employees = Employee.objects.all()
    return render(request, 'home/create_group.html', {'employees': employees})



# TODO
@login_required(login_url='users:login')
def group_list(request):
    groups = Group.objects.filter(managers=request.user.employee.managerid)
    return render(request, 'home/group_list.html', {'groups': groups})


@login_required(login_url='users:login')
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id, managers=request.user.employee.managerid)
    group.delete()
    messages.success(request, "Group has been deleted successfully.")
    return redirect('home:group_list')


@login_required(login_url='users:login')
def assign_form_to_group(request, form_id):
    form = Forms.objects.get(form_id=form_id)
    assigned_users = []
    
    if request.method == 'POST':
        if 'assign_peer_review' in request.POST:
            group_id = request.POST.get('group_id')
            if group_id: 
                return redirect('home:assign_peer_review', form_id=form_id, group_id=group_id)

        group_id = request.POST.get('group_id')
        pid_list = request.POST.get('pids', '')
 
        pid_list = [pid.strip() for pid in pid_list.split(',') if pid.strip()]
 
        if group_id:
            group = Group.objects.get(id=group_id) 
            if not FormAssignedByTo.objects.filter(manager=request.user.employee.managerid, form=form, group=group).exists():
                FormAssignedByTo.objects.create(
                    manager=request.user.employee.managerid,
                    form=form,
                    group=group,
                    assign_date=date.today()
                ) 
 
        current_user = Manager.objects.get(user=request.user)
        for pid in pid_list:
            try:
                user = Users.objects.get(pid=pid) 
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
 
    groups = Group.objects.filter(managers=request.user.employee.managerid)
    return render(request, 'home/assign_form.html', {'form': form, 'groups': groups, 'assigned_users': assigned_users})

@login_required(login_url='users:login')
def assign_peer_review(request, form_id, group_id):
    form = get_object_or_404(Forms, pk=form_id)
    group = get_object_or_404(Group, pk=group_id)
    employees = group.employees.all()
    
    if request.method == "POST": 
        for employee in employees:
            for peer in employees:
                if employee != peer:
                    FormAssignedByTo.objects.get_or_create(
                        manager=request.user.employee.managerid,
                        employee=peer,
                        form=form,
                        group=group,
                        peer_review=True
                    )
        messages.success(request, "Peer review forms have been assigned successfully.")
        return redirect('home:index')
    
    return render(request, 'home/assign_peer_review.html', {
        'form': form,
        'group': group,
    })



@login_required(login_url='users:login')
def view_forms(request):
    forms = Forms.objects.all().order_by('-form_id')
    return render(request, 'home/view_forms.html', context={'forms': forms})


@login_required(login_url='users:login')
def assigned_forms(request): 
    employee = get_object_or_404(Employee, user=request.user)
 
    assigned_forms = FormAssignedByTo.objects.filter(employee=employee).select_related('form')
 
    for assignment in assigned_forms:
        if not assignment.has_viewed:
            assignment.has_viewed = True
            assignment.form.status = 'pending'   
            assignment.save()  

    return render(request, 'home/assigned_forms.html', {'assigned_forms': assigned_forms})


@login_required(login_url='users:login')
def fill_feedback_form(request, form_id): 
    form_instance = Forms.objects.get(form_id=form_id)
 
    employee = Employee.objects.get(user=request.user)
    assignment = FormAssignedByTo.objects.filter(form=form_instance, employee=employee).first()

    if not assignment:
        messages.error(request, "You do not have permission to fill this form.")
        return redirect('home:index')
 
    questions = Questions.objects.filter(form=form_instance)

    if request.method == 'POST':
        for question in questions:
            answer_key = f'question_{question.question_id}'
            if question.question_type == 'text': 
                answer_text = request.POST.get(answer_key)
                if answer_text:
                    QuestionAnswers.objects.create(
                        question=question,
                        user=request.user,
                        answer_text=answer_text
                    )
            elif question.question_type == 'numeric': 
                answer_value = request.POST.get(answer_key)
                if answer_value: 
                    answer_entry = QuestionAnswers.objects.create(
                        question=question,
                        user=request.user,
                        answer_text=''  
                    ) 
                    NumericResponse.objects.create(
                        answer=answer_entry,
                        user=request.user,
                        answer_value=float(answer_value)  
                    )
 
        FilledForm.objects.create(
            form=form_instance,
            employee=employee
        )
 
        assignment.delete()
        form_instance.status = 'finished'
        form_instance.save()

        messages.success(request, "Your responses have been submitted successfully!")
        return redirect('home:index')

    return render(request, 'home/fill_feedback_form.html', {'form': form_instance, 'questions': questions})



@login_required(login_url='users:login')
def filled_forms(request):
    employee = Employee.objects.get(user=request.user)
    filled_forms = FilledForm.objects.filter(employee=employee).select_related('form')

    return render(request, 'home/filled_forms.html', {'filled_forms': filled_forms})
  
  
from django.http import HttpResponseRedirect

@login_required(login_url='users:login')
def assign_peer_review(request, form_id, group_id):
    form = get_object_or_404(Forms, pk=form_id)
    group = get_object_or_404(Group, pk=group_id)  
    employees = group.employees.all()
 
    groups = Group.objects.filter(managers=request.user.employee.managerid)

    if request.method == "POST": 
        for employee in employees:
            for peer in employees:
                if employee != peer:
                    FormAssignedByTo.objects.get_or_create(
                        manager=request.user.manager,
                        employee=peer,
                        form=form,
                        group=group,
                        peer_review=True
                    )
        messages.success(request, "Peer review forms have been assigned successfully.")
        
        # Redirect to the previous page
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return redirect('home:assign_form_to_group', form_id=form_id)
    return render(request, 'home/assign_peer_review.html', context={
        'form': form,
        'group': group,
        'employees': employees,
        'groups': groups  
    })
