# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0011_auto_20150709_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='purpose',
            field=models.CharField(verbose_name='purpose', null=True, blank=True, max_length=500),
        ),
    ]
