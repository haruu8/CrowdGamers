from django.urls import path
from . import views



app_name = 'clans'

urlpatterns = [
    path('', views.home, name='home'),
    path('clan/create/', views.clan_create, name='clan_create'),
    path('clan/list/', views.clan_list, name='clan_list'),
    path('clan/<str:clan_name>/', views.clan_detail, name='clan_detail'),
    path('clan/<str:clan_name>/update/', views.clan_update, name='clan_update'),
    path('clan/<str:clan_name>/delete/', views.clan_delete, name='clan_delete'),

    # 通知
    path('<str:username>/notice/apply/', views.user_apply_notice, name='user_apply_notice'),
    path('<str:username>/notice/apply/<int:pk>/', views.user_apply_notice_detail, name='user_apply_notice_detail'),
    path('<str:username>/notice/invite/', views.user_invite_notice, name='user_invite_notice'),
    path('<str:username>/notice/invite/<int:pk>/', views.user_invite_notice_detail, name='user_invite_notice_detail'),

    # リクエスト送信
    path('<str:clan_name>/clan/request/input/', views.clan_request_input, name='clan_request_input'),
    path('<str:clan_name>/clan/request/confirm/', views.clan_request_confirm, name='clan_request_confirm'),
    path('<str:clan_name>/clan/request/create/', views.clan_request_create, name='clan_request_create'),

    # 招待送信
    path('<str:username>/invite/input/', views.user_invite_input, name='user_invite_input'),
    path('<str:username>/invite/confirm/', views.user_invite_confirm, name='user_invite_confirm'),
    path('<str:username>/invite/create/', views.user_invite_create, name='user_invite_create'),
]
