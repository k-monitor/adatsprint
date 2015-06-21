# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mp',
            name='finished',
            field=models.BooleanField(verbose_name='finished', default=False),
        ),
        migrations.AddField(
            model_name='mp',
            name='verified',
            field=models.BooleanField(verbose_name='verified', default=False),
        ),
        migrations.AlterField(
            model_name='expense',
            name='VAT_amount',
            field=models.DecimalField(max_digits=10, verbose_name='VAT amount', decimal_places=2),
        ),
    ]
