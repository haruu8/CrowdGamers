from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'),
            name='account_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
            name='account_logout'),
    path('detail/<int:pk>/', views.account_detail, name='account_detail'),
    path('update/<int:pk>/', views.account_update, name='account_update'),
    path('delete/<int:pk>/', views.account_delete, name='account_delete'),
    path('settings/', views.account_settings, name='account_settings'),
]
