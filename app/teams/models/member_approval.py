from django.db import models

class MemberApproval(models.model):
    """
    メンバー追加の認可を管理する

    Notes
    -----
    has_read は既読管理
    """
    class Meta():
        db_table = 't_member_approval'
        verbose_name = 'メンバー追加認可'
        verbose_name_plural = 'メンバー追加認可'

    id = models.AutoField(primary_key=True, editable=False)
    has_read = models.BooleanField(default=False)
    is_proceeded = models.BooleanField(null=True)
