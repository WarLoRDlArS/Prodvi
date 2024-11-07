from django.urls import path
from . import views

app_name = "Brain" 

urlpatterns = [
    path('output/', views.output, name='output'), 
     path('form-data/<str:form_identifier>/', views.another_view, name='get_form_data'),
] 

