# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('created_on', models.DateTimeField(auto_now=True, verbose_name='created on')),
            ],
            options={
                'verbose_name_plural': 'campaigns',
                'verbose_name': 'campaign',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.PositiveIntegerField(verbose_name='row number')),
                ('invoice_reference', models.CharField(max_length=50, verbose_name='invoice reference')),
                ('delivery_date', models.DateField(verbose_name='delivery date')),
                ('provider', models.CharField(max_length=200, verbose_name='provider')),
                ('product', models.CharField(max_length=200, verbose_name='product')),
                ('purchase_date', models.DateField(verbose_name='purchase date')),
                ('purpose', models.CharField(blank=True, max_length=200, verbose_name='purpose')),
                ('net_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='net amount')),
                ('VAT_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='net amount')),
                ('gross_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='gross amount')),
                ('claimed_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='claimed amount')),
            ],
            options={
                'verbose_name_plural': 'expenses',
                'verbose_name': 'expense',
            },
        ),
        migrations.CreateModel(
            name='MP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('agreement_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='agreement number')),
                ('campaign_start', models.DateField(blank=True, null=True, verbose_name='campaign start')),
                ('campaign_end', models.DateField(blank=True, null=True, verbose_name='campaign end')),
                ('total', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10, verbose_name='total')),
                ('signed_on', models.DateField(blank=True, null=True, verbose_name='signed on')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('pdf_file', models.FileField(blank=True, upload_to='', verbose_name='PDF file')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('campaign', models.ForeignKey(to='campaigns.Campaign', verbose_name='campaign')),
            ],
            options={
                'verbose_name_plural': 'MPs',
                'verbose_name': 'MP',
            },
        ),
        migrations.AddField(
            model_name='expense',
            name='MP',
            field=models.ForeignKey(to='campaigns.MP', verbose_name='MP'),
        ),
    ]
