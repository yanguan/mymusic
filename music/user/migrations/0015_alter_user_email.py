# Generated by Django 3.2 on 2023-10-28 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20231028_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default=None, max_length=30, verbose_name='邮箱'),
        ),
    ]