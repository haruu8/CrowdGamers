from django.urls import path
from . import views



app_name = 'teams'

urlpatterns = [
    path('', views.home, name='home'),
    path('team/create/', views.team_create, name='team_create'),
    path('team/list/', views.team_list, name='team_list'),
    path('team/<str:teamname>/', views.team_detail, name='team_detail'),
    path('team/<str:teamname>/update/', views.team_update, name='team_update'),
    path('team/<str:teamname>/delete/', views.team_delete, name='team_delete'),

    # プロフィール
    path('<str:username>/game/', views.account_detail_game, name='account_detail_game'),
    path('<str:username>/feature/', views.account_detail_feature, name='account_detail_feature'),
    path('<str:username>/_desired_job_type/', views.account_detail_desired_job_type, name='account_detail_desired_job_type'),

    # 通知
    path('<str:username>/notification/apply/', views.user_apply_notification, name='user_apply_notification'),
    path('<str:username>/notification/apply/<int:pk>/', views.user_apply_notification_detail, name='user_apply_notification_detail'),
    path('<str:username>/notification/invite/', views.user_invite_notification, name='user_invite_notification'),
    path('<str:username>/notification/invite/<int:pk>/', views.user_invite_notification_detail, name='user_invite_notification_detail'),

    # リクエスト送信
    path('team/apply/input/', views.team_apply_input, name='team_apply_input'),
    path('team/apply/confirm/', views.team_apply_confirm, name='team_apply_confirm'),
    path('<str:teamname>/team/apply/create/', views.team_apply_create, name='team_apply_create'),

    # 招待送信
    path('invite/input/', views.user_invite_input, name='user_invite_input'),
    path('invite/confirm/', views.user_invite_confirm, name='user_invite_confirm'),
    path('<str:username>/invite/create/', views.user_invite_create, name='user_invite_create'),

    # サポートページ
    path('terms-of-service/', views.TemplateView.as_view(template_name='teams/support/terms-of-service.html'),
            name='terms-of-service'),
    path('privacy-policy/', views.TemplateView.as_view(template_name='teams/support/privacy-policy.html'),
            name='privacy-policy'),
    path('contact/', views.TemplateView.as_view(template_name='teams/support/contact.html')),
    path('faq/', views.faq, name='faq'),
]
