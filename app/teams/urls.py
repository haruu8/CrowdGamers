from django.urls import path
from . import views
from django.views.generic import TemplateView



app_name = 'teams'

urlpatterns = [
    # サポートページ
    path('', views.GetProfileView.as_view(template_name='teams/home.html'), name='home'),
    path('contact/', views.GetProfileView.as_view(template_name='teams/support/contact.html'), name='contact'),
    path('faq/', views.faq, name='faq'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    # チーム
    path('team/create/', views.team_create, name='team_create'),
    path('team/list/', views.team_list, name='team_list'),
    path('team/<str:teamname>/update/', views.team_update, name='team_update'),
    path('team/<str:teamname>/delete/', views.team_delete, name='team_delete'),

    # メンバー
    path('team/<str:teamname>/member/add/', views.team_member_add, name='team_member_add'),
    path('team/<str:teamname>/member/delete/<str:username>/', views.team_member_delete, name='team_member_delete'),

    # チームプロフィール
    path('team/<str:teamname>/', views.team_detail, name='team_detail'),
    path('team/<str:teamname>/member/', views.team_detail_member, name='team_detail_member'),
    path('team/<str:teamname>/feature/', views.team_detail_feature, name='team_detail_feature'),
    path('team/<str:teamname>/desired_condition/', views.team_detail_desired_condition, name='team_detail_desired_condition'),

    # プロフィール
    path('<str:username>/', views.account_detail_game, name='account_detail'),
    path('<str:username>/feature/', views.account_detail_feature, name='account_detail_feature'),
    path('<str:username>/desired_condition/', views.account_detail_desired_condition, name='account_detail_desired_condition'),
    path('<str:username>/update/', views.account_profile_update, name='account_profile_update'),

    # 通知
    path('<str:username>/notification/apply/', views.apply_notification, name='apply_notification'),
    path('<str:username>/notification/apply/<uuid:id>/', views.apply_notification_detail, name='apply_notification_detail'),
    path('<str:username>/notification/invite/', views.invite_notification, name='invite_notification'),
    path('<str:username>/notification/invite/<uuid:id>/', views.invite_notification_detail, name='invite_notification_detail'),

    # リクエスト送信
    path('team/<str:teamname>/apply/create/', views.apply_create, name='apply_create'),
    path('<str:username>/apply/reply/create/<uuid:id>/', views.apply_reply_create, name='apply_reply_create'),

    # 招待送信
    path('<str:username>/invite/create/', views.invite_create, name='invite_create'),
]
