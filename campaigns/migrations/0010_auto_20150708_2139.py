# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0009_auto_20150707_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mp',
            name='agreement_number',
            field=models.CharField(null=True, verbose_name='agreement number', max_length=50, blank=True),
        ),
    ]
