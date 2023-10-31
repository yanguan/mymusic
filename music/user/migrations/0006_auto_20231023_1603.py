# Generated by Django 3.2 on 2023-10-23 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='vote_time',
            field=models.CharField(default=None, max_length=12, null=True, verbose_name='投票时间'),
        ),
    ]