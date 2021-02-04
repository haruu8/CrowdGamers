# Generated by Django 3.1.5 on 2021-02-03 05:49

import clans.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('icon', models.ImageField(blank=True, upload_to=clans.models.user_directory_path, validators=[clans.models.Clan.validate_icon_image])),
                ('url', models.URLField(null=True)),
                ('description', models.CharField(max_length=255)),
                ('sponsor', models.CharField(max_length=50)),
                ('desired_condition', models.CharField(max_length=200)),
                ('disclosed', models.BooleanField(default=False, verbose_name='公開・非公開')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'クラン',
                'verbose_name_plural': 'クラン',
                'db_table': 't_clan',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'タグ',
                'verbose_name_plural': 'タグ',
                'db_table': 't_tag',
            },
        ),
        migrations.CreateModel(
            name='UserClan',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('is_owner', models.BooleanField(default=False)),
                ('desired_condition', models.CharField(max_length=255)),
                ('disclosed', models.BooleanField(default=True)),
                ('clan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clans.clan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ユーザークラン',
                'verbose_name_plural': 'ユーザークラン',
                'db_table': 't_user_clan',
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255, null=True, verbose_name='メッセージ')),
                ('invite_url', models.URLField(verbose_name='招待URL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clans.clan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clans.userclan')),
            ],
            options={
                'verbose_name': '招待',
                'verbose_name_plural': '招待',
                'db_table': 't_invite',
            },
        ),
        migrations.AddField(
            model_name='clan',
            name='feature',
            field=models.ManyToManyField(to='clans.Tag', verbose_name='特徴'),
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255, null=True, verbose_name='志望理由')),
                ('achievement', models.CharField(max_length=255, null=True, verbose_name='実績')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clans.clan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clans.userclan')),
            ],
            options={
                'verbose_name': 'リクエスト',
                'verbose_name_plural': 'リクエスト',
                'db_table': 't_apply',
            },
        ),
    ]
