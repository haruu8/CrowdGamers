from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid



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

class Team(models.Model):
    class Meta():
        db_table = 't_team'
        verbose_name = 'チーム'
        verbose_name_plural = 'チーム'

    def validate_icon_image(fieldfile_obj):
        image_size = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if image_size > megabyte_limit*1024*1024:
            raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))

    id = models.AutoField(editable=False, primary_key=True)
    team_name_regex = RegexValidator(regex=r'[a-xA-Z0-9_]')
    team_name = models.CharField(
        verbose_name='クランネーム',
        null=False,
        blank=False,
        unique=True,
        db_index=True,
        max_length=15,
        validators=[MinLengthValidator(4), team_name_regex])
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
    game_title = models.ManyToManyField(Game, related_name='team_game_title')
    feature = models.ManyToManyField(Feature, verbose_name='特徴', related_name='team_feature')
    desired_condition = models.CharField(max_length=200)
    disclosed = models.BooleanField(verbose_name='公開・非公開', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



""" ユーザープロフィールモデル """

class UserProfile(models.Model):
    class Meta():
        db_table = 't_user_profile'
        verbose_name = 'ユーザープロフィール'
        verbose_name_plural = 'ユーザープロフィール'

    def validate_icon_image(fieldfile_obj):
        image_size = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if image_size > megabyte_limit*1024*1024:
            raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))

    def validate_header_image(fieldfile_obj):
        image_size = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if image_size > megabyte_limit*1024*1024:
            raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))

    JOB_TYPE = (
        ('player', '選手'),
        ('manger', 'マネージャー'),
        ('coach', 'コーチ'),
    )

    id = models.AutoField(editable=False, primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(verbose_name='ニックネーム', max_length=100)
    icon = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        validators=[
            validate_icon_image,
        ])
    header = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        validators=[
            validate_header_image,
        ])
    date_of_birth = models.DateField(null=False, blank=False)
    is_owner = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team', null=True, blank=True)
    game_title = models.ManyToManyField(Game, related_name='user_game_title')
    introduction = models.CharField(max_length=140)
    clip_url = models.URLField(blank=True, null=True)
    desired_job_type = models.CharField(choices=JOB_TYPE, null=False, blank=False, max_length=100)
    desired_condition = models.CharField(verbose_name='希望条件', max_length=255)
    disclosed = models.BooleanField(default=True)



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

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='send_apply')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receive_apply')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    message = models.CharField(verbose_name='志望理由', max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message



""" よくある質問モデル """

class Question(models.Model):
    class Meta():
        db_table = 't_question'
        verbose_name = 'よくある質問'
        verbose_name_plural = 'よくある質問'

    id = models.UUIDField(primary_key=True, editable=False)
    question = models.CharField(max_length=255, null=False, blank=False)
    awnser = models.CharField(max_length=1000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
