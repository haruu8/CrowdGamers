from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
import uuid
from teams.utils import user_directory_path
from accounts.fields import LowerCharField


class CustomUserManager(UserManager):
    """
    ユーザーマネージャー。
    """
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        ユーザーを作成する関数

        See Also
        --------
        normalize_email : 大文字・小文字を等しく扱うメソッド
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """
    AbstractBaseUser を継承したカスタムユーザー。

    See Also
    --------
    REQUIRED_FIELDS : スーパーユーザーを作るときの必須フィールド

    Notes
    -----
    email field を用意しないと superuser を作れないため、フィールドを用意している
    """
    class Meta:
        db_table = 't_custom_user'
        verbose_name = 'カスタムユーザー'
        verbose_name_plural = 'カスタムユーザー'

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    email = models.EmailField(null=True, blank=True, editable=False)
    id = models.AutoField(primary_key=True, editable=False)
    username_regex = RegexValidator(regex=r'[a-zA-Z0-9_]')
    username = LowerCharField(
        verbose_name='ユーザーネーム',
        null=False,
        blank=False,
        unique=True,
        db_index=True,
        max_length=15,
        validators=[MinLengthValidator(4), username_regex])
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username']



@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    """
    新規ユーザー作成時に UserProfle モデルの空インスタンスを生成する関数。

    Notes
    -----
    循環インポートが起きるため、作成の段階でインポートする。
    """
    if kwargs['created']:
        from teams.models import UserProfile
        UserProfile.objects.get_or_create(user=kwargs['instance'])



@receiver(post_save, sender=User)
def create_notification(sender, **kwargs):
    """
    新規ユーザー作成時にプロフィールの編集を促す通知を作成する。

    See Also
    --------
    from_user : 公式アカウント

    Notes
    -----
    循環インポートが起きるため、作成の段階でインポートする。
    """
    if kwargs['created']:
        from teams.models import Notification
        Notification.objects.get_or_create(
            mode='official',
            from_user=User.objects.get(username='crowdgamers'),
            to_user=kwargs['instance'],
            message='プロフィールを入力をしてあなただけの素敵なプロフィールを完成させましょう！編集はヘッダーのアイコンをクリックし、プロフィール画面から行うことができます。',
        )
