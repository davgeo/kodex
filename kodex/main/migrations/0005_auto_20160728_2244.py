# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_starredmovie_starredtv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='starredmovie',
            name='id',
        ),
        migrations.RemoveField(
            model_name='starredtv',
            name='id',
        ),
        migrations.RemoveField(
            model_name='starredtv',
            name='seasonid',
        ),
        migrations.AlterField(
            model_name='starredmovie',
            name='movieid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='starredtv',
            name='tvshowid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
