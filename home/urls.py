from django.urls import path


from . import views

app_name = "home"
urlpatterns = [
    path('index/', views.index, name='index'), 
    path('logout/', views.logout_link, name='logout'),
    path("profile/", views.user_profile, name='userProfile'),
    path("createfeedbackform/", views.createfeedbackform, name='createfeedbackform'),
    path('notice/', views.NoticeView, name='notice'),
    path('add_notice/', views.add_notice, name='add_notice'), 
]
