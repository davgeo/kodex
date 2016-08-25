# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('host', models.CharField(max_length=200)),
                ('port', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=200)),
                ('pwd', models.CharField(max_length=200)),
            ],
        ),
    ]
