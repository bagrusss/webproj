# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0010_auto_20150702_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='created',
        ),
    ]
