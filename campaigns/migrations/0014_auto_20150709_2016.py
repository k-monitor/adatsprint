# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0013_auto_20150709_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='purpose',
            field=models.CharField(blank=True, verbose_name='purpose', null=True, max_length=1000),
        ),
    ]
