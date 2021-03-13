from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .team import Team
from .job import Job
from .game import Game
from .feature import Feature
from teams.utils import user_directory_path, validate_header_image, validate_icon_image



class UserProfile(models.Model):
    """
    ユーザープロフィールモデル

    Notes
    -----
    Userが作成されたら同時にオブジェクトが生成される
    """
    class Meta():
        db_table = 't_user_profile'
        verbose_name = 'ユーザープロフィール'
        verbose_name_plural = 'ユーザープロフィール'

    id = models.AutoField(editable=False, primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(
        verbose_name='ニックネーム',
        max_length=100,
        null=False,
        blank=False,
        default='ニックネーム',
    )
    icon = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        default='default/profile_icon.svg',
        validators=[
            validate_icon_image,
        ])
    header = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        default='default/profile_header.jpg',
        validators=[
            validate_header_image,
        ])
    is_owner = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='belonging_user_profiles', null=True, blank=True)
    game_title = models.ManyToManyField(Game, related_name='user_game_title')
    feature = models.ManyToManyField(Feature, related_name='profile_feature')
    introduction = models.CharField(null=True, blank=True, max_length=140)
    website = models.URLField(blank=True, null=True)
    clip_url = models.URLField(blank=True, null=True)
    desired_job = models.ManyToManyField(Job, related_name='profile_desired_job')
    desired_condition = models.CharField(verbose_name='希望条件', max_length=255)
    disclosed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
