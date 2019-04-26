# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-26 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0003_article_is_root'),
        ('authentication', '__first__'),
        ('relationships', '0004_auto_20190423_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiki.Article')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]