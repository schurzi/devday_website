# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-16 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0016_timeslot_text_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='public_image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='speaker_public', verbose_name='Public speaker image'),
        ),
    ]
