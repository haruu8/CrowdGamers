from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required



# ユーザーのプロフィール
class UserDetailView(DetailView):
    template_name = 'accounts/account_detail.html'

account_detail = UserDetailView.as_view()
