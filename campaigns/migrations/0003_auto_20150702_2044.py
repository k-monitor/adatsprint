# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaigns', '0002_auto_20150610_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='MPEvent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.CharField(verbose_name='action', max_length=50, choices=[('inserted', 'inserted'), ('process start', 'process start'), ('process done', 'process done'), ('verify start', 'verify start'), ('verify done', 'verify done')])),
                ('happened_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='happened on')),
            ],
        ),
        migrations.RemoveField(
            model_name='mp',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='mp',
            name='finished',
        ),
        migrations.RemoveField(
            model_name='mp',
            name='updated_on',
        ),
        migrations.RemoveField(
            model_name='mp',
            name='verified',
        ),
        migrations.AddField(
            model_name='mp',
            name='status',
            field=models.PositiveIntegerField(default=1, verbose_name='status', choices=[(1, 'unprocessed'), (2, 'processing'), (3, 'processed'), (4, 'verifying'), (5, 'verified')]),
        ),
        migrations.AlterField(
            model_name='mp',
            name='campaign',
            field=models.ForeignKey(related_name='participants', to='campaigns.Campaign', verbose_name='campaign'),
        ),
        migrations.AddField(
            model_name='mpevent',
            name='MP',
            field=models.ForeignKey(verbose_name='MP', to='campaigns.MP'),
        ),
        migrations.AddField(
            model_name='mpevent',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
