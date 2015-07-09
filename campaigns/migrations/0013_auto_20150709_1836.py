# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0012_auto_20150709_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='invoice_reference',
            field=models.CharField(max_length=100, blank=True, verbose_name='invoice reference'),
        ),
    ]
