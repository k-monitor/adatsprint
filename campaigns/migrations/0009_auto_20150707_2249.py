# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaigns', '0008_auto_20150707_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='mp',
            name='processed_by',
            field=models.ForeignKey(verbose_name='processed by', related_name='+', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='mp',
            name='verified_by',
            field=models.ForeignKey(verbose_name='verified by', related_name='+', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
