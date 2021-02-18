from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .team import user_directory_path



user_directory_path = user_directory_path(instance, filename)



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
    date_of_birth = models.DateField(null=True, blank=True)
    is_owner = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team', null=True, blank=True)
    game_title = models.ManyToManyField(Game, related_name='user_game_title')
    introduction = models.CharField(max_length=140)
    clip_url = models.URLField(blank=True, null=True)
    desired_job_type = models.CharField(choices=JOB_TYPE, null=False, blank=False, max_length=100)
    desired_condition = models.CharField(verbose_name='希望条件', max_length=255)
    disclosed = models.BooleanField(default=True)
