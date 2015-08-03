# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0017_expense_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='accepted',
            field=models.BooleanField(default=True, verbose_name='Accepted by authority'),
        ),
    ]
