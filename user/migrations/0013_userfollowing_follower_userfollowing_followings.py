# Generated by Django 4.0.3 on 2022-03-03 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_rename_follower_userfollowing_following_profile_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfollowing',
            name='follower',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userfollowing',
            name='followings',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]