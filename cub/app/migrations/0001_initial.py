# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('github_token', models.TextField()),
                ('github_url', models.URLField()),
                ('avatar_url', models.URLField()),
            ],
        ),
    ]
