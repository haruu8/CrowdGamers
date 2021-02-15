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

    # プロフィール
    path('<str:username>/game/', views.account_detail_game, name='account_detail_game'),
    path('<str:username>/feature/', views.account_detail_feature, name='account_detail_feature'),
    path('<str:username>/_desired_job_type/', views.account_detail_desired_job_type, name='account_detail_desired_job_type'),

    # 通知
    path('notification/apply/', views.user_apply_notice, name='user_apply_notice'),
    path('notification/apply/<int:pk>/', views.user_apply_notice_detail, name='user_apply_notice_detail'),
    path('notification/invite/', views.user_invite_notice, name='user_invite_notice'),
    path('notification/invite/<int:pk>/', views.user_invite_notice_detail, name='user_invite_notice_detail'),

    # リクエスト送信
    path('<str:clan_name>/clan/request/input/', views.clan_request_input, name='clan_request_input'),
    path('<str:clan_name>/clan/request/confirm/', views.clan_request_confirm, name='clan_request_confirm'),
    path('<str:clan_name>/clan/request/create/', views.clan_request_create, name='clan_request_create'),

    # 招待送信
    path('<str:username>/invite/input/', views.user_invite_input, name='user_invite_input'),
    path('<str:username>/invite/confirm/', views.user_invite_confirm, name='user_invite_confirm'),
    path('<str:username>/invite/create/', views.user_invite_create, name='user_invite_create'),

    # サポートページ
    path('terms-of-service/', views.TemplateView.as_view(template_name='clans/support/terms-of-service.html'),
            name='terms-of-service'),
    path('privacy-policy/', views.TemplateView.as_view(template_name='clans/support/privacy-policy.html'),
            name='privacy-policy'),
    path('contact/', views.TemplateView.as_view(template_name='clans/support/contact.html')),
    path('faq/', views.faq, name='faq'),
]
