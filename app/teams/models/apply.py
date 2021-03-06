from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid
from .profile import UserProfile
from .team import Team
from .job import Job



""" リクエストモデル """

class Apply(models.Model):
    class Meta():
        db_table = 't_apply'
        verbose_name = 'リクエスト'
        verbose_name = verbose_name_plural = 'リクエスト'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, db_index=True)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='send_apply')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='receive_apply')
    desired_job = models.ManyToManyField(Job, related_name='apply_desired_job')
    message = models.CharField(verbose_name='志望理由', max_length=255, null=False, blank=False)
    invite_url = models.URLField(verbose_name='招待URL', null=True, blank=True)

    # 既読管理
    has_read = models.BooleanField(default=False)

    # 承認・拒否の選択
    is_proceeded = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
