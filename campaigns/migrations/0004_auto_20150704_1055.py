# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_auto_20150702_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='mp',
            name='_pdf_page_count',
            field=models.PositiveIntegerField(blank=True, verbose_name='PDF page count', editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='mpevent',
            name='MP',
            field=models.ForeignKey(related_name='events', verbose_name='MP', to='campaigns.MP'),
        ),
    ]
