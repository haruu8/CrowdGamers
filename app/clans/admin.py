from django.contrib import admin
from .models import Clan, Invite, UserProfile, Apply, Feature, Game, Question

admin.site.register(Clan)
admin.site.register(Invite)
admin.site.register(Apply)
admin.site.register(UserProfile)
admin.site.register(Feature)
admin.site.register(Game)
admin.site.register(Question)
