from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required



class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'

user_detail = UserDetailView.as_view()
