# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0018_auto_20150803_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='accepted',
        ),
        migrations.AddField(
            model_name='expense',
            name='rejected',
            field=models.BooleanField(verbose_name='Rejected by authority', default=False),
        ),
    ]
