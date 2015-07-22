# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0014_auto_20150709_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='invoice_reference',
            field=models.TextField(verbose_name='invoice reference', blank=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='product',
            field=models.TextField(verbose_name='product', blank=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='provider',
            field=models.TextField(verbose_name='provider', blank=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='purpose',
            field=models.TextField(null=True, verbose_name='purpose', blank=True),
        ),
        migrations.AlterField(
            model_name='mp',
            name='agreement_number',
            field=models.CharField(null=True, verbose_name='agreement number', max_length=200, blank=True),
        ),
    ]
