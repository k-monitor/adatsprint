# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models, migrations
from django.utils import timezone


def create_verifier_group(apps, schema, with_create_permissions=True):
    """
    Create a "verifiers" group that has the "can_verify" permission.
    All user created before July 11th 2015 are automatically added to this group.
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    User = apps.get_model('auth', 'User')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    mp_content_type = ContentType.objects.get(app_label='campaigns', model='mp')
    try:  # Workaround for #23422
        can_verify = Permission.objects.get(codename='can_verify', content_type=mp_content_type)
    except Permission.DoesNotExist:
        if with_create_permissions:
            from django.contrib.auth.management import create_permissions
            assert not getattr(apps, 'models_module', None)
            apps.models_module = True
            create_permissions(apps, verbosity=0)
            apps.models_module = None
            return create_verifier_group(
                apps, schema, with_create_permissions=False)
        else:
            raise
    cutoff_date = timezone.make_aware(datetime(2015, 7, 11, 23, 59, 59))

    verifier_group = Group.objects.create(name="Verifiers")
    verifier_group.permissions.add(can_verify)

    for user in User.objects.filter(date_joined__lte=cutoff_date):
        user.groups.add(verifier_group)


def delete_verifier_group(apps, schema):
    Group = apps.get_model('auth', 'Group')
    verifier_group = Group.objects.get(name="Verifiers")
    verifier_group.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0015_auto_20150722_1840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mp',
            options={'verbose_name': 'MP', 'verbose_name_plural': 'MPs', 'permissions': (('can_verify', 'Can verify MP'),)},
        ),
        migrations.RunPython(create_verifier_group, delete_verifier_group),
    ]
