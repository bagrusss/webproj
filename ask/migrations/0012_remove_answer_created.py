# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0011_remove_question_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='created',
        ),
    ]
