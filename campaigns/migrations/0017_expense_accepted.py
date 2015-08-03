# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0016_auto_20150722_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='accepted',
            field=models.BooleanField(verbose_name='accepted', default=True),
        ),
    ]
