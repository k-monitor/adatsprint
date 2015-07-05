# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_auto_20150704_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='VAT_amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='VAT amount', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='claimed_amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='claimed amount', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='delivery_date',
            field=models.DateField(blank=True, verbose_name='delivery date', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='gross_amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='gross amount', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='invoice_reference',
            field=models.CharField(max_length=50, blank=True, verbose_name='invoice reference'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='net_amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='net amount', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='product',
            field=models.CharField(max_length=200, blank=True, verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='provider',
            field=models.CharField(max_length=200, blank=True, verbose_name='provider'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='purchase_date',
            field=models.DateField(blank=True, verbose_name='purchase date', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='purpose',
            field=models.CharField(max_length=200, blank=True, verbose_name='purpose', null=True),
        ),
    ]
