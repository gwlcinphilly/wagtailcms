# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-19 05:21
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogCategory'),
        ),
    ]
