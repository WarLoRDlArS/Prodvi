# myapp/context_processors.py

from .models import Employee

def employee_context(request):
    if request.user.is_authenticated:
        # Retrieve the employee object linked to the logged-in user
        employee = Employee.objects.filter(user=request.user).first()
        return {'employee': employee}
    return {'employee': None}
