# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160728_2244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='starredmovie',
            old_name='movieid',
            new_name='starred_id',
        ),
        migrations.RenameField(
            model_name='starredtv',
            old_name='tvshowid',
            new_name='starred_id',
        ),
    ]
