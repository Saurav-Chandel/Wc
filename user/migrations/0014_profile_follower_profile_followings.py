# Generated by Django 4.0.3 on 2022-03-03 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_userfollowing_follower_userfollowing_followings'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follower',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='followings',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
