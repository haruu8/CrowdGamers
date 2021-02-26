from django.contrib import admin
from .models import Team, Invite, UserProfile, Apply, Feature, Game, Question, Job

admin.site.register(Team)
admin.site.register(Invite)
admin.site.register(Apply)
admin.site.register(UserProfile)
admin.site.register(Feature)
admin.site.register(Game)
admin.site.register(Question)
admin.site.register(Job)
