from django.urls import path
from . import views



app_name = 'teams'

urlpatterns = [
    # サポートページ
    path('', views.TemplateView.as_view(template_name='teams/home.html'), name='home'),
    path('terms-of-service/', views.TemplateView.as_view(template_name='teams/support/terms-of-service.html'),
            name='terms-of-service'),
    path('privacy-policy/', views.TemplateView.as_view(template_name='teams/support/privacy-policy.html'),
            name='privacy-policy'),
    path('contact/', views.TemplateView.as_view(template_name='teams/support/contact.html')),
    path('faq/', teams.views.faq, name='faq'),

    # チーム
    path('team/create/', teams.views.team_create, name='team_create'),
    path('team/list/', teams.views.team_list, name='team_list'),
    path('team/<str:teamname>/', teams.views.team_detail, name='team_detail'),
    path('team/<str:teamname>/update/', teams.views.team_update, name='team_update'),
    path('team/<str:teamname>/delete/', teams.views.team_delete, name='team_delete'),

    # プロフィール
    path('<str:username>/game/', teams.views.account_detail_game, name='account_detail_game'),
    path('<str:username>/feature/', teams.views.account_detail_feature, name='account_detail_feature'),
    path('<str:username>/_desired_job_type/', teams.views.account_detail_desired_job_type, name='account_detail_desired_job_type'),

    # 通知
    path('<str:username>/notification/apply/', teams.views.user_apply_notification, name='user_apply_notification'),
    path('<str:username>/notification/apply/<int:pk>/', teams.views.user_apply_notification_detail, name='user_apply_notification_detail'),
    path('<str:username>/notification/invite/', teams.views.user_invite_notification, name='user_invite_notification'),
    path('<str:username>/notification/invite/<int:pk>/', teams.views.user_invite_notification_detail, name='user_invite_notification_detail'),

    # リクエスト送信
    path('team/apply/input/', teams.views.team_apply_input, name='team_apply_input'),
    path('team/apply/confirm/', teams.views.team_apply_confirm, name='team_apply_confirm'),
    path('team/apply/create/', teams.views.team_apply_create, name='team_apply_create'),

    # 招待送信
    path('invite/input/', teams.views.user_invite_input, name='user_invite_input'),
    path('invite/confirm/', teams.views.user_invite_confirm, name='user_invite_confirm'),
    path('invite/create/', teams.views.user_invite_create, name='user_invite_create'),
]
