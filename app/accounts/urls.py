from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'),
            name='account_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
            name='account_logout'),
    path('detail/', views.account_detail, name='account_detail'),
    path('update/', views.account_update, name='account_update'),
    path('delete/', views.account_delete, name='account_delete'),
]
