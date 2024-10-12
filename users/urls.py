from django.urls import path


from . import views

app_name = "users"
urlpatterns = [
    # path('', views.index, name='index'), 
    # stuff got removed from here to home

    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('',views.landing_page,name='landing'),
]
