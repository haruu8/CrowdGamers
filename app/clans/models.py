from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from accounts.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)



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

    FEATURE = (
        ('Daily_Activities', '毎日活動'),
    )

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
    feature = models.CharField(verbose_name='メニュー', choices=FEATURE, max_length=50)
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
    desired_condition = models.CharField(max_length=255)
    disclosed = models.BooleanField(default=True)



""" 招待モデル """

class Invite(models.Model):
    class Meta():
        db_table = 't_invite'
        verbose_name = '招待'
        verbose_name = verbose_name_plural = '招待'

    id = models.AutoField(editable=False, primary_key=True)
    user = models.ForeignKey(UserClan, on_delete=models.CASCADE)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    message = models.CharField(verbose_name='メッセージ', max_length=255, null=True, blank=False)
    invite_url = models.URLField(verbose_name='招待URL', null=False)
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
    user = models.ForeignKey(UserClan, on_delete=models.CASCADE)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    message = models.CharField(verbose_name='志望理由', max_length=255, null=True, blank=False)
    achievement = models.CharField(verbose_name='実績', max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
