from django.db import models
from django.contrib.auth import get_user_model
import uuid



class MemberApproval(models.Model):
    """
    メンバー追加の認可を管理する

    Notes
    -----
    has_read は既読管理
    is_proceeded は承認・拒否管理
    """
    class Meta():
        db_table = 't_member_approval'
        verbose_name = 'メンバー追加認可'
        verbose_name_plural = 'メンバー追加認可'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, db_index=True)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='send_member_approval')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recieve_member_approval')
    message = models.CharField(max_length=255, null=False, blank=False)
    has_read = models.BooleanField(verbose_name='既読', default=False)
    is_proceeded = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
