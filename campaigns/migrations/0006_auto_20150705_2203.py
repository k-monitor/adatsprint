# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_auto_20150705_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='VAT_amount',
            field=models.PositiveIntegerField(blank=True, verbose_name='VAT amount', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='claimed_amount',
            field=models.PositiveIntegerField(blank=True, verbose_name='claimed amount', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='gross_amount',
            field=models.PositiveIntegerField(blank=True, verbose_name='gross amount', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='net_amount',
            field=models.PositiveIntegerField(blank=True, verbose_name='net amount', null=True),
        ),
        migrations.AlterField(
            model_name='mp',
            name='total',
            field=models.PositiveIntegerField(blank=True, verbose_name='total', null=True),
        ),
    ]
