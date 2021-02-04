from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Clan, Invite, Apply
from .forms import ClanCreateForm, InviteCreateForm, ClanApplyCreateForm



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuse



class HomeView(generic.TemplateView):
    template_name = 'clans/home.html'

home = HomeView.as_view()



# クランと同時に招待の作成もする
class ClanCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clans/clan_create.html'
    model = Clan
    form_class = ClanCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

clan_create = ClanCreateView.as_view()



class ClanListView(ListView):
    template_name = 'clans/clan_list.html'
    model = Clan

clan_list = ClanListView.as_view()



class ClanUpdateView(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    template_name = 'clans/clan_update.html'
    model = Clan
    form_class = ClanCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        return redirect(self.get_success_url())

clan_update = ClanUpdateView.as_view()



class ClanDeleteView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    template_name = 'clans/clan_delete.html'
    model = Clan
    success_url = reverse_lazy('clan:home')

clan_delete = ClanDeleteView.as_view()



class ClanApplyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clans/clan_request_create.html'
    model = Apply
    form_class = ClanApplyCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

clan_request_create = ClanApplyCreateView.as_view()



class ClanRequestConfirmView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/clan_request_confirm.html'

clan_request_confirm = ClanRequestConfirmView.as_view()



class ClanRequestCompleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/clan_request_complete.html'

clan_request_complete = ClanRequestCompleteView.as_view()



class UserInviteConfirmView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/user_invite_confirm.html'

user_invite_confirm = UserInviteConfirmView.as_view()



class UserInviteCompleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/user_invite_complete.html'

user_invite_complete = UserInviteCompleteView.as_view()
