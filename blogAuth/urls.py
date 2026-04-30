from django.urls import path
from . import views

app_name = 'blogAuth'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('delete_account', views.delete_account, name='delete_account')
]