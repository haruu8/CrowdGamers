from django.urls import path
from . import views



app_name = 'clans'

urlpatterns = [
    path('', views.home, name='home'),
    path('clan/create/', views.clan_create, name='clan_create'),
    path('clan/list/', views.clan_list, name='clan_list'),
    path('clan/detail/<int:pk>/', views.clan_detail, name='clan_detail'),
    path('clan/update/<int:pk>/', views.clan_update, name='clan_update'),
    path('clan/delete/<int:pk>/', views.clan_delete, name='clan_delete'),

    # リクエスト送信
    path('clan/request/create/', views.clan_request_create, name='clan_request_create'),
    path('clan/request/confirm/', views.clan_request_confirm, name='clan_request_confirm'),
    path('clan/request/complete/', views.clan_request_complete, name='clan_request_complete'),

    # 招待送信
    path('invite/create/', views.user_invite_create, name='user_invite_create'),
    path('invite/confirm/', views.user_invite_confirm, name='user_invite_confirm'),
    path('invite/complete/', views.user_invite_complete, name='user_invite_complete'),
]
