from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Clan, Invite
from .forms import ClanCreateForm, InviteCreateForm



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
        return redirect(self.get_success_url())

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


class RequestCompleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/request_complete.html'

request_complete = RequestCompleteView.as_view()



class InviteCompleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clans/invite_complete.html'

invite_complete = InviteCompleteView.as_view()
