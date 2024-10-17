from django.contrib import admin

# Register your models here.

from .models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('empid', 'empname', 'empdept', 'managerid', 'is_manager')
    search_fields = ('empid', 'empname', 'empdept', 'managerid')
    ordering = ('empid', )

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'managerid')
    search_fields = ('user', 'managerid')
    ordering = ('managerid', )
    fieldsets = (
        (None, {
            'fields': ('user', 'managerid'),
        }),
    )


# Register the above Models
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Manager, ManagerAdmin)

@admin.register(Forms)
class FormsAdmin(admin.ModelAdmin):
    list_display = ('form_id', 'title', 'status', 'submission_date', 'review_date')
    search_fields = ('title',)
    list_filter = ('status', 'review_date')

@admin.register(FormAssignedByTo)
class FormAssignedByToAdmin(admin.ModelAdmin):
    list_display = ('manager', 'employee', 'assign_date', 'has_filled', 'has_viewed', 'form')
    search_fields = ('manager__name', 'employee__name')
    list_filter = ('has_filled', 'has_viewed')

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'form', 'question_type', 'question_text')
    search_fields = ('question_text',)
    list_filter = ('question_type',)

@admin.register(QuestionAnswers)
class QuestionAnswersAdmin(admin.ModelAdmin):
    list_display = ('answer_id', 'question', 'user', 'answer_text')
    search_fields = ('user__username', 'question__question_text')

@admin.register(NumericResponse)
class NumericResponseAdmin(admin.ModelAdmin):
    list_display = ('answer_value', 'answer', 'user')
    search_fields = ('user__username',)


# If you dont want to use decorators, somment them and uncoment the below
# admin.site.register(Forms, FormsAdmin)
# admin.site.register(FormAssignedByTo, FormAssignedByToAdmin)
# admin.site.register(Questions, QuestionsAdmin)
# admin.site.register(QuestionAnswers, QuestionAnswersAdmin)
# admin.site.register(NumericResponse, NumericResponseAdmin)



@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_on', 'posted_by')
    search_fields = ('title', 'posted_by__username')

@admin.register(NoticeStatus)
class NoticeStatusAdmin(admin.ModelAdmin):
    list_display = ('notice', 'employee', 'viewed', 'acknowledged', 'viewed_date', 'acknowledged_date')
    search_fields = ('notice__title', 'employee__empname')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
 
