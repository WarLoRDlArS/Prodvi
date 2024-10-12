from django.urls import path


from . import views

app_name = "users"
urlpatterns = [
    # path('', views.index, name='index'), 
    # stuff got removed from here to home

    path('login/', views.login_page, name='login'),
]
