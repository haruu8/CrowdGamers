from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from accounts.models import User



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



""" タグモデル """

class Feature(models.Model):
    class Meta():
        db_table = 't_feature'
        verbose_name = '特徴'
        verbose_name_plural = '特徴'

    id = models.AutoField(editable=False, primary_key=True)
    tag = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag



""" クランモデル """

class Clan(models.Model):
    class Meta():
        db_table = 't_clan'
        verbose_name = 'クラン'
        verbose_name_plural = 'クラン'

    def validate_icon_image(fieldfile_obj):
        image_size = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if image_size > megabyte_limit*1024*1024:
            raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))

    id = models.AutoField(editable=False, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    icon = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        validators=[
            validate_icon_image,
        ])
    url = models.URLField(null=True)
    description = models.CharField(max_length=255)
    sponsor = models.CharField(max_length=50)
    feature = models.ManyToManyField(Feature, verbose_name='特徴')
    desired_condition = models.CharField(max_length=200)
    disclosed = models.BooleanField(verbose_name='公開・非公開', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



""" クランに関するモデル """

class UserClan(models.Model):
    class Meta():
        db_table = 't_user_clan'
        verbose_name = 'ユーザークラン'
        verbose_name_plural = 'ユーザークラン'

    id = models.AutoField(editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    desired_condition = models.CharField(verbose_name='希望条件', max_length=255)
    disclosed = models.BooleanField(default=True)



""" 招待モデル """

class Invite(models.Model):
    class Meta():
        db_table = 't_invite'
        verbose_name = '招待'
        verbose_name = verbose_name_plural = '招待'

    id = models.AutoField(editable=False, primary_key=True)
    from_user = models.ForeignKey(UserClan, on_delete=models.CASCADE, related_name='send_invitations')
    to_user = models.ForeignKey(UserClan, on_delete=models.CASCADE, related_name='receive_invitations')
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
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



""" リクエストモデル """

class Apply(models.Model):
    class Meta():
        db_table = 't_apply'
        verbose_name = 'リクエスト'
        verbose_name = verbose_name_plural = 'リクエスト'

    id = models.AutoField(editable=False, primary_key=True)
    from_user = models.ForeignKey(UserClan, on_delete=models.CASCADE, related_name='send_apply')
    to_user = models.ForeignKey(UserClan, on_delete=models.CASCADE, related_name='receive_apply')
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    message = models.CharField(verbose_name='志望理由', max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
