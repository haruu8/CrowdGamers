from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from teams.models import Apply, UserProfile
from accounts.models import User



""" UserProfileに関するview """

class UserProfileBaseView(DetailView):
    template_name = 'teams/accounts/profile_extends_base.html'
    model = UserProfile

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)



class UserProfileDetailGameView(UserProfileBaseView):
    template_name = 'teams/accounts/account_detail_game.html'
    model = UserProfile

    # のちに修正
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['game_title'] = UserProfile.objects.get(user=self.request.user)
        return ctx

account_detail_game = UserProfileDetailGameView.as_view()



class UserProfileDetailFeatureView(UserProfileBaseView):
    template_name = 'teams/accounts/account_detail_feature.html'
    model = UserProfile

    # のちに修正
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['feature'] = UserProfile.objects.get(user=self.request.user)
        return ctx

account_detail_feature = UserProfileDetailFeatureView.as_view()



class UserProfileDetailDesiredJobTypeView(UserProfileBaseView):
    template_name = 'teams/accounts/account_detail_desired_job_type.html'
    model = UserProfile

    # のちに修正
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['desired'] = UserProfile.objects.get(user=self.request.user)
        return ctx

account_detail_desired_job_type = UserProfileDetailDesiredJobTypeView.as_view()
