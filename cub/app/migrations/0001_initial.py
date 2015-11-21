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
                ('username', models.CharField(unique=True, max_length=50)),
                ('github_token', models.TextField()),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=70)),
                ('github_url', models.URLField()),
                ('avatar_url', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('username', 'email')]),
        ),
    ]
