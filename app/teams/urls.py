from django.urls import path
from . import views



app_name = 'teams'

urlpatterns = [
    path('', views.home, name='home'),
    path('team/create/', views.team_create, name='team_create'),
    path('team/list/', views.team_list, name='team_list'),
    path('team/<str:team_name>/', views.team_detail, name='team_detail'),
    path('team/<str:team_name>/update/', views.team_update, name='team_update'),
    path('team/<str:team_name>/delete/', views.team_delete, name='team_delete'),

    # プロフィール
    path('<str:username>/game/', views.account_detail_game, name='account_detail_game'),
    path('<str:username>/feature/', views.account_detail_feature, name='account_detail_feature'),
    path('<str:username>/_desired_job_type/', views.account_detail_desired_job_type, name='account_detail_desired_job_type'),

    # 通知
    path('notification/apply/', views.user_apply_notification, name='user_apply_notification'),
    path('notification/apply/<int:pk>/', views.user_apply_notification_detail, name='user_apply_notification_detail'),
    path('notification/invite/', views.user_invite_notification, name='user_invite_notification'),
    path('notification/invite/<int:pk>/', views.user_invite_notification_detail, name='user_invite_notification_detail'),

    # リクエスト送信
    path('<str:team_name>/team/request/input/', views.team_request_input, name='team_request_input'),
    path('<str:team_name>/team/request/confirm/', views.team_request_confirm, name='team_request_confirm'),
    path('<str:team_name>/team/request/create/', views.team_request_create, name='team_request_create'),

    # 招待送信
    path('<str:username>/invite/input/', views.user_invite_input, name='user_invite_input'),
    path('<str:username>/invite/confirm/', views.user_invite_confirm, name='user_invite_confirm'),
    path('<str:username>/invite/create/', views.user_invite_create, name='user_invite_create'),

    # サポートページ
    path('terms-of-service/', views.TemplateView.as_view(template_name='teams/support/terms-of-service.html'),
            name='terms-of-service'),
    path('privacy-policy/', views.TemplateView.as_view(template_name='teams/support/privacy-policy.html'),
            name='privacy-policy'),
    path('contact/', views.TemplateView.as_view(template_name='teams/support/contact.html')),
    path('faq/', views.faq, name='faq'),
]
