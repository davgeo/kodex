# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarredMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('movieid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StarredTV',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('tvshowid', models.IntegerField()),
                ('seasonid', models.IntegerField()),
            ],
        ),
    ]
