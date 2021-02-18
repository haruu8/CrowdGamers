from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from teams.models import Apply, UserProfile
from accounts.models import User



""" UserProfileに関するview """

class UserProfileBaseView(DetailView):
    template_name = 'teams/accounts/profile_extends_base.html'
    model = User

    # def get_object(self):
    #     username = self.kwargs.get('username')
    #     return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(username=self.request.user)
        return context


# class UserProfileDetailGameView(UserProfileBaseView):
#     template_name = 'teams/accounts/account_detail_game.html'
#     model = UserProfile

class UserProfileDetailGameView(DetailView):
    template_name = 'teams/accounts/account_detail_game.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

account_detail_game = UserProfileDetailGameView.as_view()



class UserProfileDetailFeatureView(UserProfileBaseView):
    template_name = 'teams/accounts/account_detail_feature.html'

account_detail_feature = UserProfileDetailFeatureView.as_view()



class UserProfileDetailDesiredJobTypeView(UserProfileBaseView):
    template_name = 'teams/accounts/account_detail_desired_job_type.html'

account_detail_desired_job_type = UserProfileDetailDesiredJobTypeView.as_view()
