from django.contrib import admin
from .models import Clan, Invite, UserClan, Apply

admin.site.register(Clan)
admin.site.register(Invite)
admin.site.register(Apply)
admin.site.register(UserClan)
