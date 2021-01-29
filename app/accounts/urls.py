from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('user/detail/', views.user_detail, name='user_detail'),
]
