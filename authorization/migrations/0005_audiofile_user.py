# Generated by Django 4.2.6 on 2023-10-08 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authorization', '0004_alter_audiofile_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofile',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
