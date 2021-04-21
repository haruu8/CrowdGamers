from django.contrib import admin
from .models import Team, UserProfile, Feature, Game, Question, Job, Notification



class NotificationAdmin(admin.ModelAdmin):
    list_display = ['mode', 'sender_has_read', 'reciever_has_read', 'from_user', 'to_user', 'created_at', 'message']



class TeamAdmin(admin.ModelAdmin):
    list_display = ['teamname', 'disclosed', 'name', 'created_at']



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'team']



admin.site.register(Feature)
admin.site.register(Game)
admin.site.register(Job)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Question)
