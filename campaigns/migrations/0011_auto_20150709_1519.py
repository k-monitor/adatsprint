# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0010_auto_20150708_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='purpose',
            field=models.TextField(verbose_name='purpose', null=True, blank=True),
        ),
    ]
