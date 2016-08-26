# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('thumbnails', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('host', models.CharField(max_length=200)),
                ('port', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=200)),
                ('pwd', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StarredMovie',
            fields=[
                ('starred_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StarredTV',
            fields=[
                ('starred_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='config',
            name='activeServer',
            field=models.ForeignKey(to='kodidj.Server'),
        ),
    ]
