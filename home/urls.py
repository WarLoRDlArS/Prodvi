from django.urls import path


from . import views

app_name = "home"
urlpatterns = [
    path('', views.index, name='index'), 
    path('logout/', views.logout_link, name='logout'),
    path("profile/", views.user_profile, name='userProfile'),
]
