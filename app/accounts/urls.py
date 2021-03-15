from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='account_login'),
    path('signup/', views.signup, name='account_signup'),
    path('logout/', views.logout, name='account_logout'),
    path('<str:username>/delete/', views.account_delete, name='account_delete'),
    path('settings/', views.account_settings, name='account_settings'),
]
