from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid
from .profile import UserProfile
from .team import Team, Job



""" 招待モデル """

class Invite(models.Model):
    class Meta():
        db_table = 't_invite'
        verbose_name = '招待'
        verbose_name = verbose_name_plural = '招待'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='send_invitations')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receive_invitations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    desired_job = models.ManyToManyField(Job, related_name='invite_desired_job')
    message = models.CharField(verbose_name='メッセージ', max_length=255, null=True, blank=False)
    invite_url = models.URLField(verbose_name='招待URL', null=False)

    # 既読管理
    has_read = models.BooleanField(default=False)

    # 承認・拒否の選択
    is_proceeded = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
