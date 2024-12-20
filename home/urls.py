from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('index/', views.index, name='index'), 
    path('logout/', views.logout_link, name='logout'),
    path('profile/', views.user_profile, name='userProfile'),
    path('createfeedbackform/', views.createfeedbackform, name='createfeedbackform'),
    path('notice/', views.NoticeView, name='notice'),
    path('add_notice/', views.add_notice, name='add_notice'), 
    path('create-group/', views.create_group, name='create_group'),
    path('groups/', views.group_list, name='group_list'),
    path('assign-form/<int:form_id>/', views.assign_form_to_group, name='assign_form_to_group'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('forms/', views.view_forms, name='view_forms'),
    path('assigned_forms/', views.assigned_forms, name='assigned_forms'),
    path('fill_feedback_form/<int:form_id>/', views.fill_feedback_form, name='fill_feedback_form'),
    path('filled_forms/', views.filled_forms, name='filled_forms'),

    


    # URLs for notices and acknowledgment
    path('employee_notices/', views.employee_notices, name='employee_notices'),  # View employee notices
    path('acknowledge_notice/<int:notice_status_id>/', views.acknowledge_notice, name='acknowledge_notice'),  # Acknowledge notice

    
    path('create_group/', views.create_group, name='create_group'),
    path('group_list/', views.group_list, name='group_list'),  
    path('group/delete/<int:group_id>/', views.delete_group, name='delete_group'), 
    # path('assign_peer_review/<int:form_id>/', views.assign_peer_review, name='assign_peer_review'),
    path('assign_peer_review/<int:form_id>/<int:group_id>/', views.assign_peer_review, name='assign_peer_review'),

]
