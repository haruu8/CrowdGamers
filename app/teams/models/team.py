from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from . import *
from .game import Game
from .feature import Feature
from .job import Job



# user ごとに directory を分ける
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



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
    teamname_regex = RegexValidator(regex=r'[a-xA-Z0-9_]')
    teamname = models.CharField(
        verbose_name='チームネーム',
        null=False,
        blank=False,
        unique=True,
        db_index=True,
        max_length=15,
        validators=[MinLengthValidator(4), teamname_regex])
    name = models.CharField(max_length=100, null=False, blank=False)
    header = models.ImageField(
        default='default/profile_header.jpg',
        upload_to=user_directory_path,
        blank=True,
        validators=[
            validate_icon_image,
        ])
    icon = models.ImageField(
        default='default/profile_icon.png',
        upload_to=user_directory_path,
        blank=True,
        validators=[
            validate_icon_image,
        ])
    url = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=255)
    sponsor = models.CharField(max_length=100, null=True, blank=True)
    game_title = models.ManyToManyField(Game, related_name='team_game_title')
    feature = models.ManyToManyField(Feature, verbose_name='特徴', related_name='team_feature')
    desired_job = models.ManyToManyField(Job, related_name='team_desired_job')
    desired_condition = models.CharField(max_length=200)
    disclosed = models.BooleanField(verbose_name='公開・非公開')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
