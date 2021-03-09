from django.contrib import admin
from .models import Team, Invite, UserProfile, Apply, Feature, Game, Question, Job, MemberApproval



class ApplyAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'message']

class InviteAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'message']

class MemberApprovalAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'message']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['teamname', 'name', 'created_at']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'team']

admin.site.register(Apply, ApplyAdmin)
admin.site.register(Feature)
admin.site.register(Game)
admin.site.register(Invite, InviteAdmin)
admin.site.register(Job)
admin.site.register(MemberApproval, MemberApprovalAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Question)
