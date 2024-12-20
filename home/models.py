from django.db import models
 
from users.models import Users

class Employee(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    empid = models.CharField(primary_key=True, max_length=6) 
    empname = models.CharField(max_length=255)
    empdept = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    managerid = models.ForeignKey('Manager', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    doj = models.DateField(null=True, blank=True)
    is_manager = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.empid:  
            self.empid = self.user.pid 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Name: {self.empname} PID: {self.user.pid}"  


class Manager(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    # employee = models.OneToOneField(Employee, on_delete=models.CASCADE) 
    managerid = models.CharField(primary_key=True, max_length=6)   
    is_manager = models.BooleanField(default=True)
    # user_pid = models.CharField(max_length=6)

    def save(self, *args, **kwargs):
        if not self.managerid:  
            self.managerid = self.user.pid   
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Manager {self.user.username} ({self.managerid})"


class Department(models.Model):
    deptid = models.PositiveIntegerField(primary_key=True)
    dept_name = models.CharField(max_length=255)
    manager = models.OneToOneField(Manager, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.dept_name

 

class Forms(models.Model):
    FORM_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('fresh', 'Fresh'),
        ('finished', 'Finished'),
    ]
    
    form_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    review_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=FORM_STATUS_CHOICES)
    submission_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)  

    def __str__(self):
        return self.title


class Questions(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('numeric', 'Numeric'),
        ('text', 'Text'),
    ]
    
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    min_value = models.FloatField(null=True, blank=True)   
    max_value = models.FloatField(null=True, blank=True)   

    def __str__(self):
        return self.question_text



class QuestionAnswers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    answer_text = models.TextField()


class NumericResponse(models.Model):
    answer_value = models.FloatField()
    answer = models.ForeignKey(QuestionAnswers, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"Response by {self.user.username} with value {self.answer_value}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class NoticeStatus(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)
    viewed_date = models.DateTimeField(null=True, blank=True)
    acknowledged_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notice {self.notice.title} - {self.employee.empname}"


class Group(models.Model):
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField(Manager, related_name='managed_groups')
    employees = models.ManyToManyField(Employee, related_name='groups')

    def __str__(self):
        return self.name


class FormAssignedByTo(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)   
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    assign_date = models.DateField(auto_now_add=True)
    has_filled = models.BooleanField(default=False)
    has_viewed = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)   
    peer_review = models.BooleanField(default=False)  

    class Meta:
        unique_together = ('form', 'employee', 'group')

    def __str__(self):
        return f"Form {self.form.title} assigned to {self.employee.empname} for group {self.group.name}"



class FilledForm(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    filled_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Filled {self.form.title} by {self.employee.empname}"
