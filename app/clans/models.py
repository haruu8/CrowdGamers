from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from accounts.models import User
import uuid
from config import settings



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



""" タグモデル """

class Feature(models.Model):
    class Meta():
        db_table = 't_feature'
        verbose_name = '特徴'
        verbose_name_plural = '特徴'

    id = models.AutoField(editable=False, primary_key=True)
    feature = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feature



class Game(models.Model):
    class Meta():
        db_table = 't_game'
        verbose_name = 'ゲーム'
        verbose_name_plural = 'ゲーム'

    id = models.AutoField(editable=False, primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title



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
    clan_name_regex = RegexValidator(regex=r'[a-xA-Z0-9_]')
    clan_name = models.CharField(
        verbose_name='クランネーム',
        null=False,
        blank=False,
        unique=True,
        db_index=True,
        max_length=15,
        validators=[MinLengthValidator(4), clan_name_regex])
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
    game_title = models.ManyToManyField(Game, related_name='clan_game_title')
    feature = models.ManyToManyField(Feature, verbose_name='特徴', related_name='clan_feature')
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

    def validate_clip_file(fieldfile_obj):
        file_size = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))

    id = models.AutoField(editable=False, primary_key=True)
    user = models.OneToOneField(settings.SOCIAL_AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_clan')
    is_owner = models.BooleanField(default=False)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name='clan')
    game_title = models.ManyToManyField(Game, related_name='user_game_title')
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    introduction = models.CharField(max_length=140)
    clip = models.FileField(
        blank=True,
        upload_to=user_directory_path,
        validators=[
            validate_clip_file,
            FileExtensionValidator(['mp4']),
        ]
    )
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

    apply_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    from_user = models.ForeignKey(UserClan, on_delete=models.CASCADE, related_name='send_apply')
    to_user = models.ForeignKey(UserClan, on_delete=models.CASCADE, related_name='receive_apply')
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    message = models.CharField(verbose_name='志望理由', max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
