# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0007_auto_20150707_1954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='delivery_date',
            new_name='invoice_issue_date'
        ),
        migrations.AlterField(
            model_name='expense',
            name='invoice_issue_date',
            field=models.DateField(null=True, verbose_name='issue date', blank=True),
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='purchase_date',
            new_name='payment_date'
        ),
        migrations.AlterField(
            model_name='expense',
            name='payment_date',
            field=models.DateField(null=True, verbose_name='payment date', blank=True),
        ),
    ]
