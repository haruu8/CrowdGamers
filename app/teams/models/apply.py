from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid
from .profile import UserProfile
from .team import Team



""" リクエストモデル """

class Apply(models.Model):
    class Meta():
        db_table = 't_apply'
        verbose_name = 'リクエスト'
        verbose_name = verbose_name_plural = 'リクエスト'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='send_apply')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receive_apply')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    message = models.CharField(verbose_name='志望理由', max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

