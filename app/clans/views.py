from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Clan, Invite, Apply
from .forms import ClanCreateForm, UserInviteCreateForm, ClanRequestCreateForm



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



class ClanDetailView(DetailView):
    template_name = 'clans/clan_detail.html'
    model = Clan

clan_detail = ClanDetailView.as_view()



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



""" クランリクエストに関する view """

class ClanRequestInputView(LoginRequiredMixin, generic.FormView):
    template_name = 'clans/clan_request_input.html'
    form_class = ClanRequestCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

clan_request_input = ClanRequestInputView.as_view()



class ClanRequestConfirmView(LoginRequiredMixin, FormView):
    template_name = 'clans/clan_request_confirm.html'
    form_class = ClanRequestCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'clans/clan_request_input.html', {'form': form})

clan_request_confirm = ClanRequestConfirmView.as_view()



class ClanRequestCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clans/clan_request_input.html'
    form_class = ClanRequestCreateForm
    success_url = reverse_lazy('clans:home')

    # エラーページに遷移するのがいいのか
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

clan_request_create = ClanRequestCreateView.as_view()



""" ユーザー招待に関する view """

class UserInviteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clans/user_invite_create.html'
    model = Invite
    form_class = UserInviteCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

user_invite_create = UserInviteCreateView.as_view()



class UserInviteConfirmView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/user_invite_confirm.html'

user_invite_confirm = UserInviteConfirmView.as_view()



class UserInviteCompleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/user_invite_complete.html'

user_invite_complete = UserInviteCompleteView.as_view()
