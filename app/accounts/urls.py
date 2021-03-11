from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('signup/', views.LoginView.as_view(template_name='accounts/signup.html'),
            name='account_signup'),
    path('logout/', auth_views.LogoutView.as_view(),
            name='account_logout'),
    path('<str:username>/delete/', views.account_delete, name='account_delete'),
    path('settings/', views.account_settings, name='account_settings'),
]
