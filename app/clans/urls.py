from django.urls import path
from . import views



app_name = 'clans'

urlpatterns = [
    path('', views.home, name='home'),
    path('clan/create/', views.clan_create, name='clan_create'),
    path('clan/list/', views.clan_list, name='clan_list'),
    path('clan/update/<int:pk>/', views.clan_update, name='clan_update'),
    path('clan/delete/<int:pk>/', views.clan_delete, name='clan_delete'),
    path('request/complete/', views.request_complete, name='request_complete'),
    path('invite/complete/', views.invite_complete, name='invite_complete'),
]
