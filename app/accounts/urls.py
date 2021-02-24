from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'),
            name='account_login'),
    path('signup/', auth_views.LoginView.as_view(template_name='accounts/signup.html'),
            name='account_signup'),
    path('logout/', auth_views.LogoutView.as_view(),
            name='account_logout'),
    path('<str:username>/update/', views.account_update, name='account_update'),
    path('<str:username>/delete/', views.account_delete, name='account_delete'),
    path('list/', views.account_list, name='account_list'),
    path('settings/', views.account_settings, name='account_settings'),
]
