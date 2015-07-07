# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_auto_20150705_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpevent',
            name='action',
            field=models.CharField(verbose_name='action', choices=[('inserted', 'inserted'), ('process start', 'process start'), ('process done', 'process done'), ('verify start', 'verify start'), ('verify done', 'verify done'), ('process unclaim', 'process unclaim'), ('verify unclaim', 'verify unclaim')], max_length=50),
        ),
    ]
